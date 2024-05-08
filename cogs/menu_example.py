import discord
import datetime
from discord.ext import commands
from discord import app_commands

bot_avatar_img = "https://cdn.discordapp.com/attachments/1071136297533579334/1219639688026132553/1llya_AI_avatar_Men_Czech_nationality_has_glassses_on_face_litt_ce1b968d-0ce3-4157-a616-a001c51d8642.png?ex=660c08f9&is=65f993f9&hm=0c5076e7006684155e9a49ffc942b41107a46322d0eb00e18feaa7dff14c6295&"


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.value = None
        self.page_number = 1


        self.page_2 = discord.Embed(color=discord.Color.red(), title="Page 2",
                                  description="This is page 2"
                                  )
        self.page_3 = discord.Embed(color=discord.Color.red(), title="Page 3",
                                  description="This is page 3"
                                  )

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
            embed = self.page_2
            embed.set_thumbnail(url=bot_avatar_img)

            return embed

        elif self.page_number == 3:
            embed = self.page_3
            embed.set_thumbnail(url=bot_avatar_img)

            return embed

        elif self.page_number == 4:
            embed = self.page04()
            return embed

        else:
            self.page_number = 1
            embed = self.page01()
            return embed
    def page01(self):
        embed = discord.Embed(color=discord.Color.red(), title="Page 1",
                                  description="This is page 1"
                                  )
        embed.set_thumbnail(url=bot_avatar_img)
        return embed
    def page04(self):
        embed = discord.Embed(title="Player name",
                              url="https://example.com",
                              description="This is Player name statistics",
                              colour=0xc01c28)

        embed.set_author(name="1llya's bot")

        embed.add_field(name="Nationality 🌎",
                        value="Ukraine",
                        inline=True)
        embed.add_field(name="Team 🎮",
                        value="Natus Vincere",
                        inline=True)

        embed.set_image(
            url="https://img-cdn.hltv.org/playerbodyshot/4NNsZrSGWLr9mZNt0Pe3KS.png?ixlib=java-2.1.0&w=400&s=4484cc99087121a6f9877d3742717444")

        embed.set_thumbnail(
            url="https://img-cdn.hltv.org/teamlogo/9iMirAi7ArBLNU8p3kqUTZ.svg?ixlib=java-2.1.0&s=4dd8635be16122656093ae9884675d0c")
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
