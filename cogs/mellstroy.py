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
        os.environ['IMAGEIO_FFMPEG_EXE'] = '/usr/bin/ffmpeg'
        print("Loaded FFMPEG")
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


    def generate_video_sync(self, background_image_path: str, mellstroy_clip_path: str, duration: int, meme_id: str, background_song_path: str, sad: bool):
        background_image = ImageClip(background_image_path).resize((1080, 1920))
        bg_width, bg_height = background_image.size

        mellstroy_clip_initial = VideoFileClip(mellstroy_clip_path)
        meme_image = ImageClip(f"cogs/mellstroy/memes/meme_{meme_id}.jpg")

        # audio_clip = mellstroy_clip_initial.audio
        # audio_clip = afx.audio_loop(audio_clip, duration=duration)
        audio_clip = AudioFileClip(background_song_path)

        mellstroy_clip = mellstroy_clip_initial.with_position(("center", "bottom")).without_audio().loop(
            duration=duration).resize(height=960).with_audio(
            audio_clip)
        masked_clip = vfx.mask_color(mellstroy_clip, color=[53, 253, 3], threshold=100, stiffness=5)


        # meme_image = ImageClip(f"cogs/mellstroy/memes/meme_{meme_id}.jpg").resize(width=960).with_position("top").margin(top=50, opacity=0)

        # if meme_image.size[1] > 960:
            # meme_image = meme_image.resize(height=1060)
        top_margin = 50
        side_margin = 50

        meme_width, meme_height = meme_image.size
        max_height = bg_height // 2 - top_margin
        max_width = bg_width - 2 * side_margin

        # Resize the image to fit within the max_width and max_height
        if meme_width > max_width:
            meme_image = meme_image.resize(width=max_width)
            meme_width, meme_height = meme_image.size
        if meme_height > max_height:
            meme_image = meme_image.resize(height=max_height)
            meme_width, meme_height = meme_image.size

        # Calculate the centered position for the meme image with margins
        meme_x = (bg_width - meme_width) // 2
        meme_y = (bg_height // 4 - meme_height // 2) + top_margin // 2

        meme_image = meme_image.with_position((meme_x, meme_y))


        video = CompositeVideoClip([background_image, masked_clip, meme_image]).with_duration(duration)
        if sad:
            video = video.fx(vfx.multiply_color, 0.5) # Reduce contrast


        video_path = f"./cogs/mellstroy/final_video_{meme_id}.mp4"
        video.write_videofile(video_path, audio_codec="aac")

        return video_path

    async def generate_video(self, background_image_path: str, mellstroy_clip_path: str, duration: int, meme_id: str, background_song_path: str, sad: bool):
        loop = asyncio.get_running_loop()
        video_path = await loop.run_in_executor(
            self.executor,
            self.generate_video_sync,
            background_image_path,
            mellstroy_clip_path,
            duration,
            meme_id,
            background_song_path,
            sad
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
    @app_commands.describe(url="meme url (url has to compleatly lead to photo)", mellstroy_template="Choose from mellstroy templates", duration="Duration of final video", music_clip="choose song from list", sad_filter="Do you want video to look dark?")
    @app_commands.choices(mellstroy_template=[discord.app_commands.Choice(name=clip.split("_")[1].split(".")[0], value=clip) for clip in os.listdir("./cogs/mellstroy/mellstroy_clips")],
                          music_clip=[discord.app_commands.Choice(name=song_name.split(".")[0], value=song_name) for song_name in os.listdir("./cogs/mellstroy/background_songs")],
                          sad_filter=[discord.app_commands.Choice(name="yes", value=1),
                                      discord.app_commands.Choice(name="no", value=0)]

)
    async def mellstroy_slash(self, interaction: discord.Interaction, url: str, mellstroy_template: discord.app_commands.Choice[str], duration: int, music_clip: discord.app_commands.Choice[str], sad_filter: discord.app_commands.Choice[int]):
        print(os.listdir("./cogs/mellstroy/mellstroy_clips"))
        await interaction.response.defer()
        meme_id, file_path = self.get_meme(url)

        video_path = await self.generate_video("./cogs/mellstroy/background/background.jpg",
                                               f"./cogs/mellstroy/mellstroy_clips/{mellstroy_template.value}", duration, str(meme_id), f"./cogs/mellstroy/background_songs/{music_clip.value}", sad_filter.value)

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
