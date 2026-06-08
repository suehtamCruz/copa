# Copa 2026 Scheduler - Google Calendar API

Cria eventos no Google Calendar usando a API oficial do Google (OAuth2), em vez de automação de navegador.

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração (Google Cloud)

1. Acesse https://console.cloud.google.com e crie/selecione um projeto.
2. Em **APIs e Serviços > Biblioteca**, ative a **Google Calendar API**.
3. Em **APIs e Serviços > Tela de consentimento OAuth**, configure o app (tipo Externo) e adicione seu e-mail em "Usuários de teste".
4. Em **APIs e Serviços > Credenciais**, crie uma credencial **ID do cliente OAuth** do tipo **App para computador (Desktop app)**.
5. Baixe o JSON e salve como `credentials.json` na raiz do projeto.

Na primeira execução, o navegador abrirá para você autorizar o acesso. Um arquivo `token.json` será gerado e reutilizado nas próximas execuções.

## Uso

Evento único de exemplo:

```bash
python scheduler.py
```

Agendar todos os jogos da Copa 2026 a partir do JSON:

```bash
python schedule_generator.py
```

## Funcionalidades

- Autenticação OAuth2 com a Google Calendar API
- Criação de eventos com título, data, hora, fuso horário e descrição
- Renovação automática de token
- Agendamento em lote dos jogos a partir de `copa_2026_jogos.json`

## Requisitos

- Python 3.7+
- Credenciais OAuth (`credentials.json`) do Google Cloud Console

## Segurança

Não versione `credentials.json` nem `token.json` (contêm dados sensíveis).
