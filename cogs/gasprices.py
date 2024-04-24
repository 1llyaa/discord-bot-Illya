import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from discord import app_commands

bot_avatar_img = "https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&"


def get_gas_prices(city: str):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.post(f'https://www.mbenzin.cz/Ceny-benzinu-a-nafty/{city}', headers=headers)

    parsed_site = response.text

    soup = BeautifulSoup(parsed_site, "lxml")

    # divs_names = soup.find_all("div", class_="col-10")
    # divs_names_list = []
    # for name in divs_names:
    #     divs_names_list.append(name.text.strip().replace("\n", "-").replace("\r", "").replace("          ", " ".replace(",", " ")))
    #
    # print(divs_names_list)

    # Names List
    divs_names = soup.find_all("span", class_="font-s-11r")
    divs_names_list = []
    for name in divs_names:
        divs_names_list.append(name.text)

    divs_names_list = divs_names_list[: len(divs_names_list) - 3]
    # # Debug
    # print(divs_names_list)
    # print(f"Names list lenght: {len(divs_names_list)}")

    # Prices list
    divs_prices = soup.find_all("div", class_="col text-center p-1")
    divs_prices_list = []

    for price in divs_prices:
        divs_prices_list.append(price.text.strip().replace("\n", " "))

    # code made by chatGPT
    divs_prices_list = [' '.join(divs_prices_list[i:i+4]) for i in range(0, len(divs_prices_list), 4)]

    # # debug
    # print(f"Price list lenght: {len(divs_prices_list) / 4}")

    # Adress list
    span_city = soup.find_all("span", itemprop="addressLocality")
    span_adress = soup.find_all("span", itemprop="streetAddress")
    divs_adress_list = []

    for count in range(len(span_city)):
        divs_adress_list.append(f"{span_city[count].text} - {span_adress[count].text}")

    final_list = []
    for final in range(10):
        final_list.append(f"{divs_names_list[final]}, {divs_adress_list[final]}\n{divs_prices_list[final]}")
    return final_list


def gasprices_embed(city: str):
    city = "".join(city)
    # debug
    print(city)

    gas_list = get_gas_prices(city)
    description = ""
    lines_separator = "☰"

    for desc in range(len(gas_list)):
        description += f"**{gas_list[desc]}**\n**{lines_separator * 40}**\n"

    embed = discord.Embed(
        colour=discord.colour.parse_hex_number("ff0008"),
        title=f":fuelpump:Gas prices near city {city}",
        description=description

    )

    embed.set_author(name="1llya's bot")
    embed.set_thumbnail(url=bot_avatar_img)
    embed.set_footer(text=f"Original website: https://www.mbenzin.cz")

    return embed


class GasPrices(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @app_commands.command(name="gasprices", description="Get gas prices in czech city")
    @app_commands.describe(city="City in Czech republic")
    async def gasprices(self, interaction: discord.Interaction, city: str):
        embed = gasprices_embed(city)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(GasPrices(bot))
