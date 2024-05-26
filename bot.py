import os
import requests
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BOOKS_API_KEY = os.getenv('BOOKS_API_KEY')

class BookBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.api_key = BOOKS_API_KEY

    async def on_ready(self):
        print(f'{self.user} has landed')

    async def on_message(self, message):
        if message.author == self.user:
            return

        greetings = ['hello', 'hi']
        if message.content.lower() in greetings:
            await message.reply('Hello there!')
            user_name = message.author.name
            await message.channel.send(f'Hi {user_name}')

        await self.process_commands(message)


# Create bot instance with necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = BookBot(command_prefix='$', intents=intents)

# Register commands
@bot.command(name='bookInfo')
async def book_info(ctx, *args):
    await bot.book_info(ctx, *args)

bot.run(DISCORD_BOT_TOKEN)
