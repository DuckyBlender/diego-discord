# DiegoGPT Discord Bot

A simple Discord bot powered by Ollama and the fine-tuned DiegoGPT model.

## Prerequisites
- Python 3.x
- Ollama installed and running

## Setup
1. Install Ollama and make sure it's running
2. Pull the model: `ollama pull duckyblender/diegoGPT`
3. Install dependencies: `pip install -r requirements.txt`
4. Create `.env` file with `DISCORD_TOKEN=your_bot_token`
5. Run: `python bot.py`

You can also run the bot using Docker Compose:

```bash
docker-compose up
```

The docker-compose does not include ollama, so you'll still have to run it in the background.

## Features
- Responds to messages in a specific Discord channel
- Maintains conversation history via replies
- Uses Ollama for local AI inference
- Skips replies to other user members
