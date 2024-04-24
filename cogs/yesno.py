import discord
import asyncio
import random
from discord.ext import commands
from discord import app_commands


class Yesno(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @app_commands.command(name="yesno", description="yes/no decider")
    async def yesno(self, interaction: discord.Interaction):
        random_number = random.randint(0, 1)

        up = ":thumbsup:"
        down = ":thumbsdown:"

        await interaction.response.send_message(up)
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
            await interaction.edit_original_response(content=message_content)
            await asyncio.sleep(0.3)

        if random_number == 0:
            await interaction.edit_original_response(content="Result: :thumbsup:")
        else:
            await interaction.edit_original_response(content="Result: :thumbsdown:")

        # for multiplier in range(1, 10):


async def setup(bot):
    await bot.add_cog(Yesno(bot))