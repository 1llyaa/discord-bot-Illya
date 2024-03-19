import discord
import requests
from discord.ext import commands
import toml

bot_avatar_img = "https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&"
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot_channel_id = 786984140234555402

def load_config():
    with open("./config.toml", "r") as f:
        data = toml.load(f)

        token = data['config']['token']
    return token
@bot.event
async def on_ready():
    print("Hello, bot is ready!")
    channel = bot.get_channel(bot_channel_id)
    await channel.send("Hello bot is ready to work!")

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
async def commands(ctx):

    embed = discord.Embed(
        colour=discord.colour.parse_hex_number("ff0008"),
        title="**Commands you are or will be able to use**",
        description="**.hello** - Introduction of bot\n"
                    "**.commands** - Showing all commands of a bot\n"
                    "**.cs2_elo** <nickmane> - Show elo on cs2 faceit of certain player\n"
                    "**.csgo_elo** <nickmane> - Show elo on csgo faceit of certain player"
    )
    embed.set_author(name="1llya's bot")
    embed.set_thumbnail(url=bot_avatar_img)

    await ctx.send(embed=embed)

@bot.command()
async def cs2_elo(ctx, nickname: str):
    # cs2 data fetch
    url = f"https://api.satont.ru/faceit?nick={nickname}&game=cs2&timezone=Europe%2FPrague"
    cs_elo_data = requests.get(url)
    cs_elo_data = cs_elo_data.json()
    # stats
    elo = int(cs_elo_data['elo'])
    kd = cs_elo_data['stats']['lifetime']['Average K/D Ratio']
    winrate = cs_elo_data['stats']['lifetime']['Win Rate %']
    matches = cs_elo_data['stats']['lifetime']['Matches']
    wins = cs_elo_data['stats']['lifetime']['Wins']
    loses = int(matches) - int(wins)
    # TODO Check response status code example if status code is not 200 tell about it to user of bot



    # embed creation
    embed = discord.Embed(
        colour=discord.colour.parse_hex_number("ff0008"),
        title=f"**{nickname}**",
        url=f"https://faceit.com/en/players/{nickname}",
        description=f"**Elo** - {str(elo)}\n"
                    f"**Avg. K/D** - {kd}\n"
                    f"**Matches** - {matches}\n"
                    f"**Wins** - {wins}\n"
                    f"**Loses** - {loses}\n"
                    f"**Winrate** - {winrate}%"
    )
    # determinates thumbnail image
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



    await ctx.send(embed=embed)

@bot.command()
async def csgo_elo(ctx, nickname: str):
    # cs2 data fetch
    url = f"https://api.satont.ru/faceit?nick={nickname}&game=csgo&timezone=Europe%2FPrague"
    cs_elo_data = requests.get(url)
    cs_elo_data = cs_elo_data.json()
    # stats
    elo = int(cs_elo_data['elo'])
    kd = cs_elo_data['stats']['lifetime']['Average K/D Ratio']
    winrate = cs_elo_data['stats']['lifetime']['Win Rate %']
    matches = cs_elo_data['stats']['lifetime']['Matches']
    wins = cs_elo_data['stats']['lifetime']['Wins']
    loses = int(matches) - int(wins)
    # TODO Check response status code example if status code is not 200 tell about it to user of bot



    # embed creation
    embed = discord.Embed(
        colour=discord.colour.parse_hex_number("ff0008"),
        title=f"**{nickname}**",
        url=f"https://faceit.com/en/players/{nickname}",
        description=f"**Elo** - {str(elo)}\n"
                    f"**Avg. K/D** - {kd}\n"
                    f"**Matches** - {matches}\n"
                    f"**Wins** - {wins}\n"
                    f"**Loses** - {loses}\n"
                    f"**Winrate** - {winrate}%"
    )
    # determinates thumbnail image
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



    await ctx.send(embed=embed)

def main():
    discord_token = load_config()
    
    bot.run(discord_token)


if __name__ == "__main__":
    main()
