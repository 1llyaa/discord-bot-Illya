import discord
from discord.ext import commands
import toml

bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())
bot_channel_id = 786984140234555402

@bot.event
async def on_ready():
    print("Hello, bot is ready!")
    channel = bot.get_channel(bot_channel_id)
    await channel.send("Hello bot is ready to work!")

@bot.command()
async def hello(ctx):
    embed = discord.Embed(
            colour=discord.colour.parse_hex_number("997b28"),
            description="Hello, my name is 1llya's\nIm his first bot so be humble\nYou can see my commands by typing **-help**",
            title="Info about me"
            )
    embed.set_footer(text="If you click my name you can see 1llya's Github")
    embed.set_author(name="1llya", url="https://github.com/1llyaa/discord-bot-Illya")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&")

    await ctx.send(embed=embed)


def load_config():
    with open("./config.toml", "r") as f:
        data = toml.load(f)

        token = data['config']['token']
    return token

def main():
    discord_token = load_config()
    
    bot.run(discord_token)


if __name__ == "__main__":
    main()
