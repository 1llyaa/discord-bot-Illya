import discord
from discord.ext import commands
from discord import app_commands

bot_avatar_img = "https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&"


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.value = None
        self.page_number = 1

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
            embed = discord.Embed(color=discord.Color.red(), title="Page 1",
                                  description="This is page 1"
                                  )
            embed.set_thumbnail(url=bot_avatar_img)

            return embed

        elif self.page_number == 2:
            embed = discord.Embed(color=discord.Color.red(), title="Page 2",
                                  description="This is page 2"
                                  )
            embed.set_thumbnail(url=bot_avatar_img)

            return embed

        elif self.page_number == 3:
            embed = discord.Embed(color=discord.Color.red(), title="Page 3",
                                  description="This is page 3"
                                  )
            embed.set_thumbnail(url=bot_avatar_img)

            return embed

        else:
            self.page_number = 1
            embed = discord.Embed(color=discord.Color.red(), title="Page 1",
                                  description="This is page 1"
                                  )
            embed.set_thumbnail(url=bot_avatar_img)

            return embed


class MenuCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @commands.command()
    async def menu(self, ctx):
        view = Menu()
        view.add_item(discord.ui.Button(label="URL Button", style=discord.ButtonStyle.link, url="https://aitek.digital"))
        await ctx.reply("Hello this is menu", view=view)

    @app_commands.command(name="menu", description="This is test menu")
    async def menu_slash(self, interaction: discord.Interaction):
        view = Menu()

        view.add_item(discord.ui.Button(label="URL Button", emoji="🌐", style=discord.ButtonStyle.link, url="https://github.com/1llyaa/discord-bot-Illya"))
        await interaction.response.send_message(embed=view.pages(), view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(MenuCommands(bot))
