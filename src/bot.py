import discord
from discord import Client, Intents
import os
from ml_model import generate_response, load_model
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

llm, tokenizer = load_model()

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

    if message.reference and message.reference.resolved:
        if message.reference.resolved.author != bot.user:
            return
    elif message.reference:
        try:
            replied_to_message = await message.channel.fetch_message(message.reference.message_id)
            if replied_to_message.author != bot.user:
                return
        except (discord.NotFound, discord.HTTPException):
            # If the message can't be fetched, we can't verify the author, so we'll ignore it.
            return

    if str(message.channel.id) != '1394337366822617111':
        return
    
    messages = [{"role": "user", "content": message.content}]

    async with message.channel.typing():
        response = generate_response(llm, tokenizer, messages)
        await message.reply(response)

bot.run(TOKEN)