import discord
import asyncio
import toml
import os
from tinydb import TinyDB, Query
from discord.ext import commands
from discord import app_commands
from bs4 import BeautifulSoup

# current database is made just for one server, need to add function to check server id and create database based on server id.
db = TinyDB("quotes.json")
Todo = Query()

bot_avatar_img = "https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&"
bot = commands.Bot(command_prefix=".", help_command=None, intents=discord.Intents.all())
bot_channel_id = 786984140234555402


# class Menu(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.value = None
#
#     @discord.ui.button(label="Send message", style=discord.ButtonStyle.grey)
#     async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await interaction.response.send_message("embed=embed")
#
#     @discord.ui.button(label="Edit message", style=discord.ButtonStyle.green)
#     async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await interaction.response.edit_message(content="This is edited message")
#
#     @discord.ui.button(label="Edited embed", style=discord.ButtonStyle.blurple)
#     async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
#         embed = discord.Embed(color=discord.Color.random())
#         embed.set_author(name="FOO")
#         embed.add_field(name="Lol", value="Lol")
#         await interaction.response.edit_message(embed=embed)
#
#     @discord.ui.button(label="Quit", style=discord.ButtonStyle.red)
#     async def menu4(self, interaction: discord.Interaction, button: discord.ui.Button):
#         embed = discord.Embed(color=discord.Color.red())
#         embed.set_author(name="Byebye")
#         embed.add_field(name="Byebye", value="Do well")
#         await interaction.response.edit_message(embed=embed)
#         self.value = False
#         self.stop()

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            await bot.load_extension(f'cogs.{filename[:-3]}')
# @bot.command()
# async def menu(ctx):
#     view = Menu()
#     view.add_item(discord.ui.Button(label="URL Button", style=discord.ButtonStyle.link, url="https://aitek.digital"))
#     await ctx.reply("Hello this is menu", view=view)


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
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")


async def main():
    await load()
    discord_token = load_config()
    await bot.start(discord_token)


if __name__ == "__main__":
    asyncio.run(main())
