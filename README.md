# Discord Exa Bot

A Discord self-bot that answers questions using [Exa's](https://exa.ai) AI-powered answer API. Mention `@exa` followed by a question, and get instant answers sourced from the web.

## Features

- **@exa queries** - Ask any question and get AI-generated answers
- **Citation support** - Use `/links` to get sources for the last answer
- **No link previews** - Clean responses without annoying embed cards
- **Flexible permissions** - Works in any channel for you, specific channels for others

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/discord-exa-bot.git
cd discord-exa-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file:

```env
DISCORD_USER_TOKEN=your_discord_user_token
DISCORD_CHANNEL_ID=channel_id_for_others
EXA_API_KEY=your_exa_api_key
```

- **DISCORD_USER_TOKEN** - Your Discord user token ([how to get it](https://www.androidauthority.com/get-discord-token-3149920/))
- **DISCORD_CHANNEL_ID** - Channel where non-you users can use the bot
- **EXA_API_KEY** - Get one from [exa.ai](https://exa.ai)

### 4. Run locally

```bash
python discord_exa_bot.py
```

## Deploy to Railway

1. Install [Railway CLI](https://docs.railway.app/develop/cli)
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`
5. Set environment variables in the Railway dashboard

## Usage

In Discord:

```
@exa what is the capital of France?
```

Get sources for the last answer:

```
/links
```

## How it works

1. Listens for messages containing `@exa`
2. Extracts the question from the message
3. Calls Exa's `/answer` API endpoint
4. Returns the AI-generated answer (without link previews)
5. Stores citations for retrieval via `/links`

## Notes

- This is a **self-bot** (uses your user token, not a bot token)
- Discord doesn't officially support self-bots - use at your own risk
- Keep your tokens secure and never commit them to version control

## License

MIT
