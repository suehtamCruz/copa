import os
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
DEFAULT_EVENT_HOURS = 2


class CalendarScheduler:
    def __init__(self, credentials_file="credentials.json", token_file="token.json",
                 default_timezone="America/Sao_Paulo"):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.default_timezone = default_timezone
        self.service = None

    def authenticate(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Renovando token de acesso...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Arquivo '{self.credentials_file}' não encontrado. "
                        "Baixe as credenciais OAuth do Google Cloud Console."
                    )
                print("Abrindo navegador para autenticação...")
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)
        print("Autenticação concluída com sucesso!")

    def add_calendar_event(self, title, date, time_start, time_end=None,
                           description="", timezone=None, calendar_id="primary"):
        if self.service is None:
            raise RuntimeError("Chame authenticate() antes de adicionar eventos.")

        timezone = timezone or self.default_timezone
        start_dt = datetime.strptime(f"{date} {time_start}", "%Y-%m-%d %H:%M")

        if time_end and time_end != time_start:
            end_dt = datetime.strptime(f"{date} {time_end}", "%Y-%m-%d %H:%M")
        else:
            end_dt = start_dt + timedelta(hours=DEFAULT_EVENT_HOURS)

        event = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_dt.isoformat(), "timeZone": timezone},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": timezone},
        }

        print(f"Criando evento: {title}")
        created = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Evento criado: {created.get('htmlLink')}")
        return created


def main():
    scheduler = CalendarScheduler()

    try:
        scheduler.authenticate()

        scheduler.add_calendar_event(
            title="Reunião de Planejamento",
            date="2026-06-15",
            time_start="14:00",
            time_end="15:00",
            description="Discussão sobre o projeto da Copa",
        )

        print("\nProcesso concluído com sucesso!")

    except Exception as e:
        print(f"Erro: {str(e)}")


if __name__ == "__main__":
    main()
