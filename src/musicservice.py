from collections import namedtuple
import threading
from discord import VoiceClient, FFmpegPCMAudio
import discord
from youtube_dl import YoutubeDL
import utils
import exceptions
import asyncio


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

Song = namedtuple("Song", "title audio_url yt_url duration")

class MusicService:
    def __init__(self):
        self.voice_client: VoiceClient = None
        self.queue = []

    # INTERFACE #

    async def play(self, ctx, *, song_names: list):
        voice = ctx.author.voice
        if not voice:
            raise exceptions.UserNotConnectedToVoiceChannel()

        if not self.is_connected_to(voice.channel):
            await self.connect_or_move_to(channel=voice.channel)
        
        for song_name in song_names:
            self.add_song(ctx, song_name)
            
        if not self.is_playing():
            self.play_next(ctx)


    async def skip(self, ctx):
        if self.is_playing():
            await ctx.send("Song skipped!")
            await ctx.message.add_reaction(u"\U0001F44C")
            self.voice_client.stop()
    

    async def queued_songs(self, ctx):
        song_titles = [ f"{i}. {self.song_description(song)}" for i, song in enumerate(self.queue, start = 1) ]
        message = '\n'.join(song_titles)
        await utils.embeded_message(ctx, message=message if message else "Queue is empty")


    # PRIVATE #

    def is_playing(self):
        return self.voice_client is not None and self.voice_client.is_playing()


    def is_connected_to(self, channel):
        return self.voice_client is not None and self.voice_client.channel == channel and self.voice_client.is_connected()


    def search_yt(self, *, song_name):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                song = ydl.extract_info("ytsearch:%s" % song_name, download=False)['entries'][0]
            except:
                raise exceptions.InvalidSongName(song_name)

        yt_url = f"https://www.youtube.com/watch?v={song['id']}"
        return Song(song["title"], song["url"], yt_url, song["duration"])


    async def connect_or_move_to(self, *, channel):
        if self.voice_client is None or not self.voice_client.is_connected():
            self.voice_client = await channel.connect()
        else:
            self.voice_client.move_to(channel)

        
    def empty_queue(self):
        return not self.queue


    async def play_next(self, ctx):
        if self.empty_queue():
            await self.leave(ctx)
            return

        song = self.queue.pop(0)
        await utils.embeded_message(ctx, action="Playing", message=self.song_description(song))
        self.voice_client.play(FFmpegPCMAudio(song.audio_url, **FFMPEG_OPTIONS))

        # Wait till finished
        while self.is_playing():
            await asyncio.sleep(1)

        await self.play_next(ctx)


    async def leave(self, ctx):
        await ctx.send("Bye bye")
        await self.voice_client.disconnect()


    def song_description(self, song):
        hours = int(song.duration / 3600)
        minutes = int(song.duration / 60)
        seconds = song.duration % 60

        def padd(n):
            return f"0{n}" if n < 10 else str(n)

        return f"[{song.title}]({song.yt_url}) -> {padd(hours)}:{padd(minutes)}:{padd(seconds)}"


    async def add_song(self, ctx, song_name):
        song = self.search_yt(song_name=song_name)
        self.queue.append(song)
        await utils.embeded_message(ctx, action="Queued", message=self.song_description(song), color=discord.Colour.green(), blame=ctx.author)

