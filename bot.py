import os
import requests
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BOOKS_API_KEY = os.getenv('BOOKS_API_KEY')

class BookBot(commands.Bot):
    def __init__(self, intents):
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)
        self.api_key = BOOKS_API_KEY
        self.synced = False

    async def setup_hook(self):
        # Register the slash commands
        self.tree.add_command(book_info)
        self.tree.add_command(say_hi)  # Register the /hi command
        await self.tree.sync()

    async def on_ready(self):
        if not self.synced:
            await self.tree.sync()
            self.synced = True
        print(f'{self.user} has landed')

@app_commands.command(name='bookinfo', description='Fetches book information based on author or title')
@app_commands.describe(query='The search query for the book (author or title)')
async def book_info(interaction: discord.Interaction, query: str):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={BOOKS_API_KEY}'
    response = requests.get(url)
    books = response.json().get('items', [])

    if not books:
        await interaction.response.send_message("No books found.")
        return

    embed = discord.Embed(title="Book Search Results", description="Here are the books found:", color=discord.Color.blue())
    for i, book in enumerate(books, 1):
        volume_info = book['volumeInfo']
        title = volume_info.get('title', 'No title available')
        authors = volume_info.get('authors', ['No author available'])
        authors_str = ", ".join(authors)
        embed.add_field(name=f'{i}. {title}', value=f'Author(s): {authors_str}', inline=False)

    await interaction.response.send_message(embed=embed)

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await interaction.client.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await interaction.followup.send('No response, search stopped.')
        return

    selection = int(msg.content)
    if selection == -1:
        await interaction.followup.send('Search stopped.')
        return

    if 1 <= selection <= len(books):
        selected_book = books[selection - 1]
        volume_info = selected_book['volumeInfo']
        title = volume_info.get('title', 'No title available')
        authors = volume_info.get('authors', ['No author available'])
        description = volume_info.get('description', 'No description available')
        average_rating = volume_info.get('averageRating', 'No rating available')
        authors_str = ", ".join(authors)
        detail_embed = discord.Embed(title=title, description=description, color=discord.Color.green())
        detail_embed.add_field(name="Author(s)", value=authors_str, inline=False)
        detail_embed.add_field(name="Average Rating", value=average_rating, inline=False)
        await interaction.followup.send(embed=detail_embed)
    else:
        await interaction.followup.send('Invalid selection.')

@app_commands.command(name='hi', description='Responds with a hello')
async def say_hi(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

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
