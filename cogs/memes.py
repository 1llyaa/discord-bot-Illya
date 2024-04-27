import requests
import discord
from discord.ext import commands
from discord import app_commands

# used API: https://github.com/D3vd/Meme_Api


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://meme-api.com/gimme"

    def get_meme(self):
        response = requests.get(url=self.url)
        url_data = response.json()['url']

        return url_data

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @app_commands.command(name="meme", description="Random meme from reddit")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.get_meme())


async def setup(bot):
    await bot.add_cog(Memes(bot))
