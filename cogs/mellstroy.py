import discord
from discord.ext import commands
from discord import app_commands


class Mellstroy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @commands.command()
    async def mellstroy(self, ctx):
        file = discord.File("/home/illya/Workspace/Python/Doma/mellstory-video-test/final_video.mp4")
        await ctx.send(file=file, content="Mellstroy video")

    @app_commands.command(name="mellstroy")
    async def mellstroy_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello this is test slash command {interaction.user.name}")


async def setup(bot):
    await bot.add_cog(Mellstroy(bot))
