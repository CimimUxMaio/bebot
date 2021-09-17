from collections import namedtuple
from discord import VoiceClient
import discord
from song import Song
import utils
import exceptions
import asyncio


QueuedSong = namedtuple("QueuedSong", "song blame")

class MusicService:
    def __init__(self):
        self.voice_client: VoiceClient = None
        self._queue = []


    # INTERFACE #

    async def play(self, ctx, *, search_string):
        voice = ctx.author.voice
        if not voice:
            raise exceptions.UserNotConnectedToVoiceChannel()

        if not self.is_connected():
            await self.connect(voice.channel)
        
        await self.add_song(ctx, search_string)
            
        if not self.is_playing():
            await self.play_loop(ctx)


    async def skip(self, ctx, song_index):
        if len(self._queue)-1 < song_index or song_index < 0:
            raise exceptions.IndexOutOfBoundaries(song_index + 1)

        if song_index == 0:
            self.voice_client.stop()

        event = "Removed" if song_index > 0 else "Skipped"
        queued_song = self._queue.pop(song_index)

        await ctx.message.add_reaction(u"\U0001F44C")
        await self.notify_song_event(ctx, event, queued_song, show_blame=True)
        
#        if song_index > 0:
#            queued_song = self._queue.pop(song_index)
#            await self.notify_song_event(ctx, "Removed", queued_song, show_blame=True)
#        elif self.is_playing() and song_index == 0:
#            await self.notify_song_event(ctx, "Skipped", queued_song=self._queue[0], show_blame=True)
#            self.voice_client.stop()
    

    async def show_queue(self, ctx):
        song_titles = [ f"{i}. {queued_song.song.description}" for i, queued_song in enumerate(self._queue, start = 1) ]
        message = '\n'.join(song_titles)
        embed = utils.embeded_message(message=message if message else "Queue is empty")
        await ctx.send(embed=embed)

    # PRIVATE #

    def is_playing(self):
        return self.voice_client is not None and self.voice_client.is_playing()


    def is_connected(self):
        return self.voice_client is not None and self.voice_client.is_connected()


    async def connect(self, voice_channel):
        self.voice_client = await voice_channel.connect()


    def empty_queue(self):
        return not self._queue


    async def play_loop(self, ctx):
        if self.empty_queue():
            await self.leave(ctx)
            return

        queued_song = self._queue[0]
        await self.notify_song_event(ctx, "Playing", queued_song, show_blame=True)
        self.voice_client.play(queued_song.song.audio())

        await self.wait_finish_playing()

        self._queue.pop(0)
        await self.play_loop(ctx)

    
    async def wait_finish_playing(self):
        while self.is_playing():
            await asyncio.sleep(1)


    async def leave(self, ctx):
        await ctx.send("Bye bye")
        self._queue = []
        await self.voice_client.disconnect()


    async def add_song(self, ctx, song_name):
        queued_song = QueuedSong(Song(song_name), utils.Blamed(ctx.author))
        self._queue.append(queued_song)
        await self.notify_song_event(ctx, "Queued", queued_song, color=discord.Colour.green())


    async def notify_song_event(self, ctx, event, queued_song, color=discord.Colour.blue(), show_blame=False):
        embed = utils.embeded_message(
            event=event, 
            message=queued_song.song.description, 
            color=color, 
            blame=queued_song.blame if show_blame else None
        )

        await ctx.send(embed=embed)