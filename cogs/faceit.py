import discord
import requests
from discord.ext import commands
from discord import app_commands


class FaceitEloCheck:
    def __init__(self, game: str, nickname: str):
        self.game = game
        self.nickname = nickname

    def get_faceit_data_embed(self):
        # cs2 data fetch
        url = f"https://api.satont.ru/faceit?nick={self.nickname}&game={self.game}&timezone=Europe%2FPrague"
        cs_elo_data = requests.get(url)

        if cs_elo_data.status_code == 200:
            # debug
            # print("response status code 200")

            cs_elo_data = cs_elo_data.json()
            # stats
            elo = int(cs_elo_data['elo'])
            kd = cs_elo_data['stats']['lifetime']['Average K/D Ratio']
            winrate = cs_elo_data['stats']['lifetime']['Win Rate %']
            matches = cs_elo_data['stats']['lifetime']['Matches']
            wins = cs_elo_data['stats']['lifetime']['Wins']
            loses = int(matches) - int(wins)

            embed = discord.Embed(
                colour=discord.colour.parse_hex_number("ff0008"),
                title=f"**{self.nickname}**",
                url=f"https://faceit.com/en/players/{self.nickname}",
                description=f"**Elo** - {str(elo)}\n"
                            f"**Avg. K/D** - {kd}\n"
                            f"**Matches** - {matches}\n"
                            f"**Wins** - {wins}\n"
                            f"**Loses** - {loses}\n"
                            f"**Winrate** - {winrate}%")

            if elo > 2001:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit10.png")
            elif elo > 1751:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit9.png")
            elif elo > 1531:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit8.png")
            elif elo > 1351:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit7.png")
            elif elo > 1201:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit6.png")
            elif elo > 1051:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit5.png")
            elif elo > 901:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit4.png")
            elif elo > 751:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit3.png")
            elif elo > 501:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit2.png")
            elif elo > 100:
                embed.set_thumbnail(url="https://leetify.com/assets/images/rank-icons/faceit1.png")

        else:
            embed = discord.Embed(
                colour=discord.colour.parse_hex_number("ff0008"),
                title=f"**{self.nickname}**",
                description=f"**Player was not found**\n"
                            f"Possible causes: {self.nickname} have never played {self.game} or player under this nickname doesnt exist"
            )

        return embed


class Faceit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    # @commands.command()
    # async def ping(self, ctx):
    #     await ctx.send("Pong")

    # @app_commands.command(name="test")
    # async def test(self, interaction: discord.Interaction):
    #     await interaction.response.send_message(f"Hello this is test slash command {interaction.user.mention}")
    @app_commands.command(name="faceitelo", description="Check elo of certain player on faceit")
    @app_commands.describe(game="Choose from cs2 and csgo", nickname="Your nickname on faceit")
    @app_commands.choices(game=[
        discord.app_commands.Choice(name="CS2", value="cs2"),
        discord.app_commands.Choice(name="CSGO", value="csgo")
    ])
    async def faceitelo(self, interaction: discord.Interaction, game: discord.app_commands.Choice[str], nickname: str):
        embed = FaceitEloCheck(game.value, nickname).get_faceit_data_embed()
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Faceit(bot))
