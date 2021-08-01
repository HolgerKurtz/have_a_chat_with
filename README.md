# Have a Chat With

Chatbot that simulates a conversation with any famous person. Dead or Alive.

## GPT-NEO

Fueled by GPT-NEO via the Huggingface API

## How To

1. Send /person NAME to start a conversation with NAME
2. That's it. 

You can change your current conversation partner by sending /person ANOTHER NAME

### Stop the bot

- ctl + c stops the telegram bot. 

## Installation

- Create a Telegram Bot for a TOKEN
- Get a HUGGINGFACE API Token (freemium version available!)
- Create a telegram_creds.json with those keys:

```json 
{
  "Token" : "YOUR BOT TOKEN",
  "HUGGINGFACE_API" : "YOUR HUGGINGFACE API TOKEN",
  "DEVELOPER_CHAT_ID" : YOUR_CHAT_ID
}
```

- ```python3 -m venv env ```
- ```pip install -r requirements ```
- ```python telegram_artist_ai.py ```

Now the bot is up and running
