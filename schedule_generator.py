import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
MATCHES_FILE = BASE_DIR / "copa_2026_jogos.json"

load_dotenv(BASE_DIR / ".env")

MAILGUN_DOMAIN = os.getenv("DOMAIN")
MAILGUN_API_KEY = os.getenv("API_KEY")
EMAIL_FROM = f"Mailgun Sandbox <postmaster@{MAILGUN_DOMAIN}>"
EMAIL_TO = "Matheus Cruz <matheuscz3110@gmail.com>"
REMINDER_MINUTES = 10
CHECK_INTERVAL_SECONDS = 60


def load_matches():
    with open(MATCHES_FILE, encoding="utf-8-sig") as file:
        return json.load(file)["matches"]


def get_match_start(match):
    timezone = ZoneInfo(match["timezone"])
    return datetime.strptime(
        f'{match["date"]} {match["time"]}',
        "%Y-%m-%d %H:%M",
    ).replace(tzinfo=timezone)


def build_email(match):
    start = get_match_start(match)
    teams = f'{match["home_team"]} x {match["away_team"]}'

    return {
        "from": EMAIL_FROM,
        "to": EMAIL_TO,
        "subject": f"Jogo começando em {REMINDER_MINUTES} minutos: {teams}",
        "text": (
            f"O jogo {teams} começa em {REMINDER_MINUTES} minutos.\n\n"
            f"Data: {start.strftime('%d/%m/%Y')}\n"
            f"Horário: {start.strftime('%H:%M')} ({match['timezone']})\n"
            f"Fase: {match['phase']}\n"
            f"Estádio: {match['stadium']}\n"
            f"Cidade: {match['city']}, {match['country']}"
        ),
    }


def send_match_email(match):
    if not MAILGUN_DOMAIN:
        raise ValueError("Variável de ambiente DOMAIN não configurada.")

    if not MAILGUN_API_KEY:
        raise ValueError("Variável de ambiente API_KEY não configurada.")

    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data=build_email(match),
        timeout=30,
    )


def wait_and_send_reminders():
    matches = sorted(load_matches(), key=get_match_start)

    for match in matches:
        start = get_match_start(match)
        reminder_at = start - timedelta(minutes=REMINDER_MINUTES)
        teams = f"{match['home_team']} x {match['away_team']}"

        while True:
            now = datetime.now(start.tzinfo)
            wait_seconds = (reminder_at - now).total_seconds()

            if wait_seconds <= 0:
                break

            minutes_remaining = int(wait_seconds // 60)
            print(f"Aguardando lembrete de {teams}. Faltam cerca de {minutes_remaining} minutos.")
            time.sleep(min(wait_seconds, CHECK_INTERVAL_SECONDS))

        if datetime.now(start.tzinfo) >= start:
            print(
                f"Lembrete ignorado porque o horário já passou: "
                f"{teams}"
            )
            continue

        response = send_match_email(match)

        if response.ok:
            print(f"E-mail enviado: {teams}")
        else:
            print(
                f"Erro ao enviar e-mail do jogo {teams}: "
                f"{response.status_code} - {response.text}"
            )


if __name__ == "__main__":
    try:
        wait_and_send_reminders()
    except KeyboardInterrupt:
        print("\nAgendamento interrompido pelo usuário.")
