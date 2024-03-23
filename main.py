import discord
import requests
import random
import asyncio
from discord.ext import commands
import toml

bot_avatar_img = "https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&"
bot = commands.Bot(command_prefix=".", help_command=None ,intents=discord.Intents.all())
bot_channel_id = 786984140234555402



def load_config():
    with open("./config.toml", "r") as f:
        data = toml.load(f)

        token = data['config']['token']
    return token

def get_faceit_data_embed(game:str, nickname: str):
    # cs2 data fetch
    url = f"https://api.satont.ru/faceit?nick={nickname}&game={game}&timezone=Europe%2FPrague"
    cs_elo_data = requests.get(url)
    
    if cs_elo_data.status_code == 200:
        print("response status code 200")
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
        title=f"**{nickname}**",
        url=f"https://faceit.com/en/players/{nickname}",
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
        title=f"**{nickname}**",
        description=f"**Player was not found**\n"
        f"Possible causes: {nickname} have never played {game} or player under this nickname doesnt exist"
        )

    return embed

@bot.event
async def on_ready():
    print("Hello, bot is ready!")
    channel = bot.get_channel(bot_channel_id)
    await channel.send("Hello bot is ready to work!")

@bot.command()
async def yesno(ctx):
    random_number = random.randint(0, 1)

    up = ":thumbsup:"
    down = ":thumbsdown:"

    message = await ctx.send(up)
    # My code
    # await message.edit(content=up)
    # await asyncio.sleep(0.3)
    # await message.edit(content=up + down)
    # await asyncio.sleep(0.3)
    # await message.edit(content=up + down + up)
    # await asyncio.sleep(0.3)
    # await message.edit(content=up + down + up + down)
    # await asyncio.sleep(0.3)
    # await message.edit(content=up + down + up + down + up)
    # await asyncio.sleep(0.3)
    # Chat gpts code based on my code
    message_content = ""
    for i in range(1, 6):
        message_content += up if i % 2 != 0 else down
        await message.edit(content=message_content)
        await asyncio.sleep(0.3)
    
    if random_number == 0:
        await message.edit(content="Result: :thumbsup:")
    else:
        await message.edit(content="Result: :thumbsdown:")

    # for multiplier in range(1, 10):

        



@bot.command()
async def hello(ctx):
    embed = discord.Embed(
            colour=discord.colour.parse_hex_number("ff0008"),
            description="Hello, my name is 1llya's\nIm his first bot so be humble\nYou can see my commands by typing **.commands**",
            title="Info about me"
            )
    embed.set_footer(text="If you click my name you can see 1llya's Github")
    embed.set_author(name="1llya", url="https://github.com/1llyaa/discord-bot-Illya")
    embed.set_thumbnail(url=bot_avatar_img)

    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):

    embed = discord.Embed(
        colour=discord.colour.parse_hex_number("ff0008"),
        title="**Commands you are or will be able to use**",
        description="**.hello** - Introduction of bot\n"
                    "**.help** - Show this embed\n"
                    "**.cs2_elo** `<nickmane>` - Show elo on cs2 faceit of certain player\n"
                    "**.csgo_elo** `<nickmane>` - Show elo on csgo faceit of certain player\n"
                    "**__.valorant_rank__** - Show valorant rank\n"
                    "**.yesno** - Yes/no :thumbsup:/:thumbsdown:"
    )

    embed.set_author(name="1llya's bot")
    embed.set_thumbnail(url=bot_avatar_img)
    embed.set_footer(text=f"Commands with underline will be avalible in the future")

    await ctx.send(embed=embed)

@bot.command()
async def cs2_elo(ctx, nickname: str):
    # cs2
    embed = get_faceit_data_embed("cs2", nickname)
    await ctx.send(embed=embed)

@bot.command()
async def csgo_elo(ctx, nickname: str):
    # cs2 data fetch
    embed = get_faceit_data_embed("csgo", nickname)
    await ctx.send(embed=embed)

def main():
    discord_token = load_config()
    
    bot.run(discord_token)


if __name__ == "__main__":
    main()
