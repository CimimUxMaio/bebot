import exceptions
from discord import VoiceClient
import discord
from discord.ext import commands
from music.SongQueue import SongQueue
import utils
import asyncio


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
        return self.is_loaded and self.voice_client.is_playing()


    @property
    def is_loaded(self):
        """ A song is loaded """
        return bool(self.voice_client and self.current)


    @property
    def is_paused(self):
        return self.is_loaded and self.voice_client.is_paused()


    async def play_loop(self):
        while True:
            self.next_song_event.clear()

            try:
                self.current = await asyncio.wait_for(self._queue.get(), timeout=20)
            except asyncio.TimeoutError:
                self.bot.loop.create_task(self.finish())
                return

            await self.notify_song_event(self.current.ctx, "Playing", self.current, show_blame=True)
            self.voice_client.play(self.current.audio(), after=self.play_next_song)

            await self.next_song_event.wait()


    def play_next_song(self, error=None):
        self.current = None
        self.next_song_event.set()

        if error:
            raise Exception(str(error))
        

    def skip(self, index):
        if not self.is_loaded:
            raise exceptions.NothingCurrentlyLoaded()

        if index == 0:
            skipped = self.current
            self.voice_client.stop()
        else:
            skipped = self._queue.pop(index-1)

        return skipped

    
    async def leave(self):
        self.audio_player.cancel()
        await self.finish()

    
    def pause(self):
        if not self.is_playing:
            raise exceptions.NothingCurrentlyPlaying()

        self.voice_client.pause()


    def resume(self):
        if not self.is_paused:
            raise exceptions.NothingCurrentlyPaused()

        self.voice_client.resume()


    async def queue_song(self, song):
        await self._queue.put(song) 


    def shuffle_queue(self):
        self._queue.shuffle()

    
    def current_lyrics(self):
        if not self.is_loaded:
            raise exceptions.NothingCurrentlyLoaded()

        lyrics = self.current.lyrics
        if not lyrics:
            raise exceptions.LyricsNotFound(self.current.title)

        return lyrics


    def purge_queue(self):
        self._queue.clear()


    async def finish(self):
        self._queue.clear()
        self.current = None
        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None


    async def notify_song_event(self, ctx, event, song, color=discord.Colour.blue(), show_blame=False):
        embed = utils.embedded_message(
            event=event, 
            message=song.description, 
            color=color, 
            blame=ctx.author if show_blame else None
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