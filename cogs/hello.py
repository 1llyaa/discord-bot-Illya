import discord
from discord.ext import commands
from discord import app_commands

bot_avatar_img = "https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&"


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @app_commands.command(name="hello", description="Interaction with bot")
    async def hello(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour=discord.colour.parse_hex_number("ff0008"),
            description="Hello, my name is 1llya's\nIm his first bot so be humble\nYou can see my commands by typing **/help**",
            title="Info about me"
        )
        embed.set_footer(text="If you click my name you can see 1llya's Github")
        embed.set_author(name="1llya", url="https://github.com/1llyaa/discord-bot-Illya")
        embed.set_thumbnail(url=bot_avatar_img)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Hello(bot))
