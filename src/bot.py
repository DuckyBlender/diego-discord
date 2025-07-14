from discord import Client, Intents
import os
from ml_model import generate_response, load_model
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

model, tokenizer, cache = load_model()

intents = Intents.default()
intents.messages = True
intents.message_content = True

bot = Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if str(message.channel.id) != '1394337366822617111':
        return

    async with message.channel.typing():
        response = generate_response(model, tokenizer, message.content, cache)
        await message.reply(response)

bot.run(TOKEN)