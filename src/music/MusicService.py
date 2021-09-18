from discord import VoiceClient
import discord
from discord.ext import commands
from music.SongQueue import SongQueue
import utils
import asyncio
from async_timeout import timeout


class MusicService:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_client: VoiceClient = None
        self._queue = SongQueue()
        self.current = None
        self.next_song_event = asyncio.Event()
        self.init_audio_player()


    @property
    def queue(self):
        return self._queue


    @property
    def is_playing(self):
        return bool(self.voice_client and self.current)


    async def play_loop(self):
        while True:
            self.next_song_event.clear()

            try:
                self.current = await asyncio.wait_for(self._queue.get(), timeout=5)
            except asyncio.TimeoutError:
                self.bot.loop.create_task(self.finish())
                return

            await self.notify_song_event(self.current.ctx, "Playing", self.current, show_blame=True)
            self.voice_client.play(self.current.audio(), after=self.play_next_song)

            await self.next_song_event.wait()


    def play_next_song(self, error=None):
        if error:
            raise Exception(str(error))
        
        self.current = None
        self.next_song_event.set()


    def skip(self, index):
        if self.is_playing and index == 0:
            skipped = self.current
            self.voice_client.stop()
        else:
            skipped = self._queue.pop(index-1)

        return skipped


    async def queue_song(self, song):
        await self._queue.put(song) 


    async def finish(self):
        self._queue.clear()
        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None


    async def notify_song_event(self, ctx, event, song, color=discord.Colour.blue(), show_blame=False):
        embed = utils.embedded_message(
            event=event, 
            message=song.description, 
            color=color, 
            blame=utils.Blamed(ctx.author) if show_blame else None
        )

        await ctx.send(embed=embed)
        
    
    async def connect(self, voice_channel):
        if self.audio_player.done():
            self.init_audio_player()

        if self.voice_client:
            await self.voice_client.move_to(voice_channel)
            return
        
        self.voice_client = await voice_channel.connect()
    

    def init_audio_player(self):
        self.audio_player = self.bot.loop.create_task(self.play_loop())