import asyncio
import discord
import uuid
import requests
import os
from discord.ext import commands
from discord import app_commands
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip, vfx, afx
from concurrent.futures import ThreadPoolExecutor


class Mellstroy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.executor = ThreadPoolExecutor(max_workers=4)

    def get_meme(self, url):
        meme_id = uuid.uuid4()
        response = requests.get(url)

        file_path = f"./cogs/mellstroy/memes/meme_{meme_id}.jpg"

        print(response)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
        return meme_id, file_path

    def generate_video_sync(self, background_image_path: str, mellstroy_clip_path: str, duration: int, meme_id: str):
        background_image = ImageClip(background_image_path).resize((1080, 1920))
        mellstroy_clip_initial = VideoFileClip(mellstroy_clip_path)

        audio_clip = mellstroy_clip_initial.audio
        audio_clip = afx.audio_loop(audio_clip, duration=duration)

        mellstroy_clip = mellstroy_clip_initial.set_position(("center", "bottom")).without_audio().loop(
            duration=duration).resize(height=960).fx(vfx.mask_color, color=[53, 253, 3], thr=100, s=5).set_audio(
            audio_clip)

        meme_image = ImageClip(f"cogs/mellstroy/memes/meme_{meme_id}.jpg").resize(width=980).set_position("top")

        video = CompositeVideoClip([background_image, mellstroy_clip, meme_image]).set_duration(duration).fadein(2)
        video_path = f"./cogs/mellstroy/final_video_{meme_id}.mp4"
        video.write_videofile(video_path)

        return video_path

    async def generate_video(self, background_image_path: str, mellstroy_clip_path: str, duration: int, meme_id: str):
        loop = asyncio.get_running_loop()
        video_path = await loop.run_in_executor(
            self.executor,
            self.generate_video_sync,
            background_image_path,
            mellstroy_clip_path,
            duration,
            meme_id
        )
        return video_path

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} command loaded")

    @commands.command()
    async def mellstroy(self, ctx, url: str):
        meme_id, file_path = self.get_meme(url)

        video_path = await self.generate_video("./cogs/mellstroy/background/background.jpg",
                                               "./cogs/mellstroy/mellstroy_clips/mellstroy_amam.mp4", 5, str(meme_id))

        file = discord.File(video_path)
        await ctx.send(file=file, content=f"{meme_id}")

        if os.path.exists(file_path):
            os.remove(file_path)

    @app_commands.command(name="mellstroy")
    @app_commands.describe(url="meme url (url has to compleatly lead to photo)", mellstroy_template="Choose from mellstroy templates", duration="Duration of final video")
    @app_commands.choices(mellstroy_template=[
        discord.app_commands.Choice(name="amamam", value="mellstroy_amam.mp4"),
        discord.app_commands.Choice(name="classy", value="mellstroy_classy.mp4"),
        discord.app_commands.Choice(name="coffe", value="mellstroy_coffe.mp4"),
        discord.app_commands.Choice(name="devil laught", value="mellstroy_hahaha.mp4"),
        discord.app_commands.Choice(name="realisation", value="mellstroy_realisation.mp4"),
        discord.app_commands.Choice(name="shocked", value="mellstroy_shocked.mp4")
    ])
    async def mellstroy_slash(self, interaction: discord.Interaction, url: str, mellstroy_template: discord.app_commands.Choice[str], duration: int):
        await interaction.response.defer()
        meme_id, file_path = self.get_meme(url)

        video_path = await self.generate_video("./cogs/mellstroy/background/background.jpg",
                                               f"./cogs/mellstroy/mellstroy_clips/{mellstroy_template.value}", duration, str(meme_id))

        file = discord.File(video_path)

        await interaction.followup.send(file=file, content=f"{meme_id}")

        if os.path.exists(file_path):
            os.remove(file_path)


    async def cog_command_error(self, ctx, error):
        print(error)
        await ctx.send("error")

    async def cog_app_command_error(self, interaction: discord.Interaction, error):
        print(error)
        await interaction.response.send_message(error)


async def setup(bot):
    await bot.add_cog(Mellstroy(bot))
