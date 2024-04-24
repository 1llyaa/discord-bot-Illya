import discord
import datetime
import random
from discord.ext import commands
from discord import app_commands
from tinydb import TinyDB, Query

db = TinyDB("./quotes.json")
Todo = Query()


def date():
    date = datetime.datetime.now()
    date = date.strftime("%d.%m.%Y")
    return date


class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @app_commands.command(name="quote-add", description="Add quote to database")
    @app_commands.describe(quote="Quote to add")
    async def quote_add(self, interaction: discord.Interaction, quote: str):
        quotes_per_user = 20
        # quote = ""
        # for words in quote:
        #     quote += f"{words} "
        #
        # quote = quote[:-1]

        username = interaction.user.name
        db.insert({'author': username, 'quote': quote, 'date': date()})

        records_count = len(db.search(Todo["author"] == username))
        # debug
        # print(f"count of records for user {username}: {records_count}")

        if records_count >= quotes_per_user:
            await interaction.response.send_message(f"You have reached max count of quotes ({quotes_per_user})")
        else:
            if len(quote) > 500:
                await interaction.response.send_message("Quote is too long!!! Max lenght is 500")
            else:
                # debug
                # print(f"username: {username} quote: {quote}")

                db.insert({'author': username, 'quote': quote, 'date': date()})
                print(username)
                print(quote)
                print(date())
                await interaction.response.send_message("Quote was sucesfully added to server database")

    @app_commands.command(name="quote-random", description="Send random quote")
    async def quote_random(self, interaction: discord.Interaction):
        quotes = db.all()
        random_quote = random.choice(quotes)
        blank_space = "  "
        # debug
        print(quotes)
        print(random.choice(quotes))
        print(f"Author: {random_quote['author']}, Quote: {random_quote['quote']}, Date: {random_quote['date']}")

        embed = discord.Embed(
            colour=discord.colour.parse_hex_number("ff0008"),
            description=f"*{random_quote['quote']}*",
        )
        embed.set_footer(
            text=f"{random_quote['date']}\n{blank_space * len(random_quote['quote'])} - {random_quote['author']}")
        # embed.set_author(name=f"{random_quote['author']}")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Quotes(bot))
