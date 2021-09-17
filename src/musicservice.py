from collections import namedtuple
from discord import VoiceClient, FFmpegPCMAudio
import discord
from youtube_dl import YoutubeDL
import utils
import exceptions
import asyncio


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

Song = namedtuple("Song", "title audio_url yt_url duration blame")

class MusicService:
    def __init__(self):
        self.voice_client: VoiceClient = None
        self._queue = []

    # INTERFACE #

    async def play(self, ctx, *, song_name):
        voice = ctx.author.voice
        if not voice:
            raise exceptions.UserNotConnectedToVoiceChannel()

        if not self.is_connected():
            self.voice_client = await voice.channel.connect()
        
        await self.add_song(ctx, song_name)
            
        if not self.is_playing():
            await self.play_loop(ctx)


    async def skip(self, ctx, song_index):
        if len(self._queue)-1 < song_index or song_index < 0:
            raise exceptions.IndexOutOfBoundaries(song_index)
        
        if song_index > 0:
            song = self._queue.pop(song_index)
            await self.send_embeded_song_message(ctx, action="Removed", song=song, show_blame=True)
        elif self.is_playing() and song_index == 0:
            await self.send_embeded_song_message(ctx, action="Skipped", song=self._queue[0], show_blame=True)
            await ctx.message.add_reaction(u"\U0001F44C")
            self.voice_client.stop()
    

    async def show_queue(self, ctx):
        song_titles = [ f"{i}. {self.song_description(song)}" for i, song in enumerate(self._queue, start = 1) ]
        message = '\n'.join(song_titles)
        embed = utils.embeded_message(message=message if message else "Queue is empty")
        ctx.send(embed=embed)

    # PRIVATE #

    def is_playing(self):
        return self.voice_client is not None and self.voice_client.is_playing()


    def is_connected(self):
        return self.voice_client is not None and self.voice_client.is_connected()


    def is_connected_to(self, channel):
        return self.is_connected() and self.voice_client.channel == channel


    def song(self, *, song_name, blame=None):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                song = ydl.extract_info("ytsearch:%s" % song_name, download=False)['entries'][0]
            except:
                raise exceptions.InvalidSongName(song_name)

        yt_url = f"https://www.youtube.com/watch?v={song['id']}"
        return Song(song["title"], song["url"], yt_url, song["duration"], blame)


    async def connect_or_move_to(self, *, channel):
        if self.voice_client is None or not self.voice_client.is_connected():
            self.voice_client = await channel.connect()
        else:
            await self.voice_client.move_to(channel)

        
    def empty_queue(self):
        return not self._queue


    async def play_loop(self, ctx):
        if self.empty_queue():
            await self.leave(ctx)
            return

        song = self._queue[0]
        await self.send_embeded_song_message(ctx, action="Playing", song=song, show_blame=True)
        self.voice_client.play(FFmpegPCMAudio(song.audio_url, **FFMPEG_OPTIONS))

        # Wait till finished
        while self.is_playing():
            await asyncio.sleep(1)

        self._queue.pop(0)
        await self.play_loop(ctx)


    async def leave(self, ctx):
        await ctx.send("Bye bye")
        self._queue = []
        await self.voice_client.disconnect()


    def song_description(self, song):
        hours = int(song.duration / 3600)
        minutes = int(song.duration / 60)
        seconds = song.duration % 60

        def padd(n):
            return f"0{n}" if n < 10 else str(n)

        return f"[{song.title}]({song.yt_url}) ({padd(hours)}:{padd(minutes)}:{padd(seconds)})"


    async def add_song(self, ctx, song_name):
        song = self.song(song_name=song_name, blame=ctx.message.author)
        self._queue.append(song)
        await self.send_embeded_song_message(ctx, action="Queued", song=song, color=discord.Colour.green())


    async def send_embeded_song_message(self, ctx, *, action, song, color=discord.Colour.blue(), show_blame=False):
        embed = utils.embeded_message(
            action=action, 
            message=self.song_description(song), 
            color=color, 
            blame=song.blame if show_blame else None
        )

        await ctx.send(embed=embed)
        
