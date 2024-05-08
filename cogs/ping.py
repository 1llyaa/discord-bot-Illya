import discord
from discord.ext import commands
from discord import app_commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello this is test slash command {interaction.user.name}")


async def setup(bot):
    await bot.add_cog(Ping(bot))
