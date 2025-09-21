import discord
from discord import Client, Intents
import os
from ollama import chat, ChatResponse
from dotenv import load_dotenv
import re

load_dotenv()

ALLOWED_CHANNELS = [
    '1394337366822617111', # DiegoGPT Testing
    '1418887616996311041' # Unmapped Nest
]

TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables")

MODEL = "duckyblender/diegoGPT"

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

    if message.type not in [discord.MessageType.default, discord.MessageType.reply]:
        return

    if str(message.channel.id) not in ALLOWED_CHANNELS:
        print(f"Ignoring message from unauthorized channel: {message.channel.id} ({message.channel.name})")
        return

    print(f"Processing message from allowed channel: {message.channel.id} ({message.channel.name})")
    messages = []
    is_reply_to_bot = False

    # Check if the message is a reply and to the bot
    if message.reference:
        try:
            # Prefer resolved message object if available
            replied_to_message = message.reference.resolved
            if not replied_to_message:
                replied_to_message = await message.channel.fetch_message(message.reference.message_id)

            if replied_to_message.author == bot.user:
                is_reply_to_bot = True
        except (discord.NotFound, discord.HTTPException):
            pass # Can't fetch message, so treat as not a reply to the bot

    if is_reply_to_bot:
        # It's a reply to the bot, build conversation history
        current_message = message
        depth = 0
        while current_message and depth < 10:
            role = "assistant" if current_message.author == bot.user else "user"
            messages.insert(0, {"role": role, "content": current_message.content})

            if not current_message.reference:
                break

            try:
                if current_message.reference.resolved:
                    current_message = current_message.reference.resolved
                else:
                    # Fetch if not cached
                    current_message = await current_message.channel.fetch_message(current_message.reference.message_id)
                depth += 1
            except (discord.NotFound, discord.HTTPException):
                break # Stop if we can't fetch a message in the chain

    else:
        # Not a reply to the bot, treat as a new conversation
        # But first, ensure it's not a reply to another user
        if message.reference:
            return # It's a reply, but not to the bot, so ignore.

        messages.append({"role": "user", "content": message.content})

    if not messages:
        return

    async with message.channel.typing():
        print("Messages being sent to model:")
        print(messages)
        response = generate_response(messages)
        await message.reply(response)

def generate_response(messages):
    try:
        response: ChatResponse = chat(model=MODEL, messages=messages, think=False)
        content = response.message.content or ''
        print(f"Raw response content: {repr(content)}")
        cleaned_content = re.sub(r'<think[^>]*>.*?</think>', '', content, flags=re.DOTALL).strip()
        print(f"Cleaned content: {repr(cleaned_content)}")  # Debug: Print cleaned content
        return cleaned_content
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return "Sorry, I'm having trouble generating a response right now."


bot.run(TOKEN)
