import discord
import datetime
import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
from discord.ext import commands
from discord import app_commands

bot_avatar_img = "https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&"
ua = "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"

db_hltv = TinyDB("./databases/hltv_players.json")
db_hltv.default_table_name = '_names'
User = Query()

headers = {
    'User-Agent': f'{ua}',
}

cached_results = {}
def get_hltv_data(nickname: str):
    player = db_hltv.search(User.name == nickname)
    player_url = dict(player[0])["url"]

    response = requests.get(player_url, headers=headers)
    response_settings = requests.get(f"https://prosettings.net/players/{nickname}/", headers=headers)

    if response.status_code != 200:
        # debug status code
        # print(response.status_code)
        get_hltv_data(nickname)
    else:
        data = response.text
        soup = BeautifulSoup(data, "lxml")
        soup2 = BeautifulSoup(response_settings.text, "lxml")

        player_stats = soup.find_all("div", class_="stats-row")
        player_stats_dict = {}
        for player_stat in player_stats:
            player_stats_dict.update(
                {player_stat.select("span")[0].text.replace(" ", "").replace("Rating1.0", "Rating").replace("Rating2.0", "Rating"): player_stat.select("span")[1].text})

        player_bodyshot_png = soup2.find("img", class_="attachment-player_bio_card size-player_bio_card wp-post-image edge-images-img edge-images-img--eager").get("src")

        try:
            real_name = soup.find(class_="summaryBodyshot").get("alt")
        except AttributeError:
            real_name = soup.find(class_="summarySquare").get("alt")
        try:
            age = soup.find(class_="summaryPlayerAge").text
        except AttributeError:
            age = None

        try:
            team = soup.find(class_="a-reset text-ellipsis").text
        except AttributeError:
            team = "No team"

        try:
            kast = soup.find_all(class_="summaryStatBreakdownDataValue")[2].text
        except AttributeError:
            kast = None

        try:
            impact = soup.find_all(class_="summaryStatBreakdownDataValue")[3].text
        except AttributeError:
            impact = None

        flag = soup.find(class_="flag").get("title")

        player_stats_dict.update({"PlayerBodyShot": player_bodyshot_png, "RealName": real_name, "Age": age, "Team": team, "KAST": kast, "IMPACT": impact, "Flag": flag})

        if player_stats_dict == {}:
            get_hltv_data(nickname)
        else:
            # print(player_stats_dict)
            # dict(player_stats_dict)["Totalkills"]
            return player_stats_dict
class Menu(discord.ui.View):
    def __init__(self, name: str, player_stats_dict: dict):
        super().__init__()
        self.value = None
        self.page_number = 1
        self.name = name
        self.player_stats_dict = player_stats_dict



    @discord.ui.button(emoji="⬅", style=discord.ButtonStyle.grey)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page_number -= 1
        await interaction.response.edit_message(embed=self.pages())

    @discord.ui.button(emoji="➡", style=discord.ButtonStyle.grey)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page_number += 1
        await interaction.response.edit_message(embed=self.pages())


    def pages(self):
        if self.page_number == 1:
            embed = self.page01()
            return embed

        elif self.page_number == 2:
            embed = self.page02()
            return embed

        elif self.page_number == 3:
            embed = self.page03()
            return embed

        else:
            self.page_number = 1
            embed = self.page01()
            return embed
    def page01(self):
        embed = discord.Embed(title=self.name.capitalize(),
                              description=f"{dict(self.player_stats_dict)["RealName"]}",
                              colour=0xc01c28)

        embed.set_author(name="1llya's bot")

        embed.add_field(name="Nationality 🌎",
                        value=f"{dict(self.player_stats_dict)["Flag"]}",
                        inline=True)
        embed.add_field(name="Team 🎮",
                        value=f"{dict(self.player_stats_dict)["Team"]}",
                        inline=True)
        embed.add_field(name="Age 🎂",
                        value=f"{dict(self.player_stats_dict)["Age"]}",
                        inline=True)

        embed.set_image(
            url=dict(self.player_stats_dict)["PlayerBodyShot"])

        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/3/3e/HLTV_2017_Logo.png")
        return embed

    def page02(self):
        embed = discord.Embed(title="Main statistics",
                              colour=0xc01c28)

        embed.set_author(name="1llya's bot")

        embed.add_field(name="**Rating**",
                        value=f"**{dict(self.player_stats_dict)["Rating"]}**",
                        inline=True)
        embed.add_field(name="**DPR**",
                        value=f"**{dict(self.player_stats_dict)["Deaths/round"]}**",
                        inline=True)
        embed.add_field(name="**KAST**",
                        value=f"**{dict(self.player_stats_dict)["KAST"]}**",
                        inline=True)
        embed.add_field(name="**IMPACT**",
                        value=f"**{dict(self.player_stats_dict)["IMPACT"]}**",
                        inline=True)
        embed.add_field(name="**ADR**",
                        value=f"**{dict(self.player_stats_dict)["Damage/Round"]}**",
                        inline=True)
        embed.add_field(name="**KPR**",
                        value=f"**{dict(self.player_stats_dict)["Kills/round"]}**",
                        inline=True)

        embed.set_image(url="https://upload.wikimedia.org/wikipedia/en/3/3e/HLTV_2017_Logo.png")

        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/3/3e/HLTV_2017_Logo.png")
        return embed
    def page03(self):
        embed = discord.Embed(title="Other statistics",
                              url="https://www.hltv.org/stats/players/7998/s1mple",
                              colour=0xc01c28)

        embed.set_author(name="1llya's bot")

        embed.add_field(name="**Total kills**",
                        value=f"**{dict(self.player_stats_dict)["Totalkills"]}**",
                        inline=True)
        embed.add_field(name="**Headshot %**",
                        value=f"**{dict(self.player_stats_dict)["Headshot%"]}**",
                        inline=True)
        embed.add_field(name="**Total deaths**",
                        value=f"**{dict(self.player_stats_dict)["Totaldeaths"]}**",
                        inline=True)
        embed.add_field(name="**K/D**",
                        value=f"**{dict(self.player_stats_dict)["K/DRatio"]}**",
                        inline=True)
        embed.add_field(name="**DMG/R**",
                        value=f"**{dict(self.player_stats_dict)["Damage/Round"]}**",
                        inline=True)
        embed.add_field(name="**G DMG/R**",
                        value=f"**{dict(self.player_stats_dict)["Grenadedmg/Round"]}**",
                        inline=True)
        embed.add_field(name="**Maps played**",
                        value=f"**{dict(self.player_stats_dict)["Mapsplayed"]}**",
                        inline=True)

        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/3/3e/HLTV_2017_Logo.png")


        return embed

class MenuHLTV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @app_commands.command(name="hltvstats", description="Check HLTV stats of your favourite player")
    @app_commands.describe(nickname="nickname of certain player")
    async def menu_slash(self, interaction: discord.Interaction, nickname: str):
        if nickname in cached_results:
            player_stats_dict = cached_results[nickname]
        else:
            # If not cached, retrieve data using get_hltv_data function
            player_stats_dict = get_hltv_data(nickname)
            # Cache the result
            cached_results[nickname] = player_stats_dict
        view = Menu(nickname, player_stats_dict)
        view.add_item(discord.ui.Button(label="URL Button", emoji="🌐", style=discord.ButtonStyle.link, url="https://github.com/1llyaa/discord-bot-Illya"))
        await interaction.response.send_message(embed=view.pages(), view=view, ephemeral=True)

    async def cog_command_error(self, ctx, error):
        print(error)
        await ctx.send("error")
    async def cog_app_command_error(self, interaction: discord.Interaction, error):
        print(error)
        await interaction.response.send_message(error)




async def setup(bot):
    await bot.add_cog(MenuHLTV(bot))
