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

    async def book_info(self, ctx, *args):
        if not args:
            await ctx.send("Please provide the book author's name.")
            return

        query = '+'.join(args)
        url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={self.api_key}'
        response = requests.get(url)
        books = response.json().get('items', [])

        if not books:
            await ctx.send("No books found.")
            return

        for i, book in enumerate(books, 1):
            volume_info = book['volumeInfo']
            title = volume_info.get('title', 'No title available')
            authors = volume_info.get('authors', ['No author available'])
            authors_str = ", ".join(authors)
            await ctx.send(f'{i}. [Title]: {title}\n\t[Author]: {authors_str}')

        await ctx.send('Choose one, enter -1 to stop')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send('No response, search stopped.')
            return

        selection = int(msg.content)
        if selection == -1:
            await ctx.send('Search stopped.')
            return

        if 1 <= selection <= len(books):
            selected_book = books[selection - 1]
            volume_info = selected_book['volumeInfo']
            title = volume_info.get('title', 'No title available')
            authors = volume_info.get('authors', ['No author available'])
            description = volume_info.get('description', 'No description available')
            average_rating = volume_info.get('averageRating', 'No rating available')
            authors_str = ", ".join(authors)
            await ctx.send(f'[Title]: {title}\n[Author]: {authors_str}\n[Description]: {description}\n[Average Rating]: {average_rating}')
        else:
            await ctx.send('Invalid selection.')

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
