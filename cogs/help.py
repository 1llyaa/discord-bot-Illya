import discord
from discord.ext import commands
from discord import app_commands

bot_avatar_img = "https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&"


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @app_commands.command(name="help", description="Help command")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            colour=discord.colour.parse_hex_number("ff0008"),
            title="**Commands you are or will be able to use**",
            description="**/hello** - Introduction of bot\n"
                        "**/help** - Shows this embed\n"
                        "**/faceitelo** `<nickmane>` - Show elo on cs2/csgo faceit of certain player\n"
                        "**/yesno** - Yes/no :thumbsup:/:thumbsdown:\n"
                        "**/quote_add** - adds quote to the server\n"
                        "**/quote_random** - sends random quote\n"
                        "**/gas_prices** `<city>` - sends gas prices in Czechia city. Example: __/gas_prices__ Praha"

        )

        embed.set_author(name="1llya's bot")
        embed.set_thumbnail(url=bot_avatar_img)
        embed.set_footer(text=f"Commands with underline will be avalible in the future")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
