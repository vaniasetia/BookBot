# BookBot

BookBot is a simple discord bot that helps you get information about books! It uses the Google Books API to fetch book information based on user queries. The bot is written in python suing the `Discord.py` library.

## Usage

1. Add the bot to your server.
2. Say hi! Write `/hi` on the server to be greeted by the bot.
3. Use the `/bookinfo` command to search for books. For example, `/bookinfo Harry Potter` will return all titles related to Harry Potter.
4. Select a book by typing the number corresponding to the book you want to know more about, or enter `-1` to stop the search.
5. The bot will display the title, author, description, and rating of the selected book.

## Installation

To install the bot, follow these steps:
1. Register a bot application on the Discord Developer Portal.
2. Make a bot with the messages intent enabled.
3. Copy the bot token.
4. Register a project on Google Cloud and add the Google Books API to the project.
5. Copy the API key.
6. Clone this repository.
7. Install requirements by running 
```
pip install -r requirements.txt
```
8. Create a `.env` file in the root directory and add your bot token in the following format:
```
DISCORD_BOT_TOKEN=<YOUR_BOT_TOKEN>
BOOKS_API_KEY=<YOUR_GOOGLE_BOOKS_API_KEY>
```
9. Run the bot using the command `python bot.py`.
