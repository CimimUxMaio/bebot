from discord import VoiceClient, FFmpegPCMAudio
import discord
from youtube_dl import YoutubeDL
import utils
import exceptions
import asyncio


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


class MusicService:
    def __init__(self):
        self.voice_client: VoiceClient = None

        self.queue = []

    # INTERFACE #

    async def play(self, ctx, *, song_name: str):
        voice = ctx.author.voice
        if not voice:
            raise exceptions.UserNotConnectedToVoiceChannel()

        await self.connect_or_move_to(channel=voice.channel)
        
        song = self.search_yt(song_name=song_name)
        self.queue.append(song)
        await utils.embeded_message(ctx, action="Queued", message=song["title"], color=discord.Colour.green(), blame=ctx.author)

        if not self.is_playing():
            await self.play_next(ctx)


    async def skip(self, ctx):
        if self.is_playing():
            await ctx.send("Song skipped!")
            await ctx.message.add_reaction(u"\U0001F44C")
            self.voice_client.stop()
    

    async def songs_queued(self, ctx):
        song_titles = [ song["title"] for song in self.queue ]
        message = '\n'.join(song_titles)
        await utils.embeded_message(ctx, message=message)

    # PRIVATE #

    def is_playing(self):
        return self.voice_client is not None and self.voice_client.is_playing()

    def is_connected_to(self, channel):
        return self.voice_client.is_connected() and self.voice_client.channel == channel

    def search_yt(self, *, song_name):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                song = ydl.extract_info("ytsearch:%s" % song_name, download=False)['entries'][0]
            except:
                raise exceptions.InvalidSongName(song_name)

        return song

    async def connect_or_move_to(self, *, channel):
        if self.voice_client is None:
            self.voice_client = await channel.connect()
        elif not self.is_connected_to(channel):
            self.voice_client.move_to(channel)

    def empty_queue(self):
        return not self.queue

    async def play_next(self, ctx):
        if self.empty_queue():
            await self.leave(ctx)
            return

        song = self.queue.pop(0)
        song_url = song["formats"][0]["url"]
        await utils.embeded_message(ctx, action="Playing", message=song["title"])
        self.voice_client.play(FFmpegPCMAudio(song_url, **FFMPEG_OPTIONS))

        # Wait till finished
        while self.is_playing():
            await asyncio.sleep(1)

        await self.play_next(ctx)


    async def leave(self, ctx):
        await ctx.send("Bye bye")
        await self.voice_client.disconnect()


INSTANCE: MusicService = MusicService()