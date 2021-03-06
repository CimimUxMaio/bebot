from discord.colour import Colour
from cogs.BaseCog import BaseCog
import exceptions
from discord.ext import commands
import config
from music.MusicService import MusicService
from music.Song import Song
from music.SongQueue import SongQueue
import utils


class MusicCog(BaseCog, name="Music"):
    def __init__(self, bot):
        super().__init__(bot)
        self.services = {}
        self.OK_EMOJI = u"\U0001F44C"

    
    @commands.command(aliases=["s"], help=config.command_help("skip"))
    async def skip(self, ctx, position: int = 0):
        skipped = ctx.music_service.skip(position)
        await ctx.send(embed=utils.embedded_message(
            event="Skipped",
            message=skipped.description,
            blame=ctx.author
        ))
    
    
    @commands.command(aliases=["q"], help=config.command_help("queue"))
    async def queue(self, ctx):
        if not ctx.music_service.current:
            await ctx.send(embed=utils.embedded_message(message="Queue is empty"))
            return 

        queue: SongQueue = ctx.music_service.queue
        header = utils.bold(f"Current: {ctx.music_service.current.description}")

        if queue.empty():
            await ctx.send(embed=utils.embedded_message(message=header))
            return

        queued = [ f"{pos}. {song.description}" for pos, song in enumerate(queue, start=1) ]
        pages = [ utils.embedded_message(message=f"{header}\n\n" + "\n".join(group)) for group in self.group_elements(queued, 5) ]

        await self.show_pages(ctx, pages=pages)

    
    @commands.command(aliases=["p"], help=config.command_help("play"))
    async def play(self, ctx, *, search):
        destination = ctx.author.voice.channel
        await ctx.music_service.connect(destination)

        async with ctx.typing():
            song = Song(ctx, search)
            await ctx.music_service.queue_song(song)
            await ctx.send(embed=utils.embedded_message(
                event="Queued",
                message=song.description,
                color=Colour.green(),
                blame=ctx.author
            ))

    
    @commands.command(help=config.command_help("pause"))
    async def pause(self, ctx):
        ctx.music_service.pause()
        await ctx.send(embed=utils.embedded_message(
            event="Paused",
            message=ctx.music_service.current.description,
            blame=ctx.author
        ))


    @commands.command(help=config.command_help("resume"))
    async def resume(self, ctx):
        ctx.music_service.resume()
        await ctx.send(embed=utils.embedded_message(
            event="Resumed",
            message=ctx.music_service.current.description,
            blame=ctx.author
        ))

    
    @commands.command(aliases=["sh"], help=config.command_help("shuffle"))
    async def shuffle(self, ctx):
        ctx.music_service.shuffle_queue()


    @commands.command(aliases=["l"], help=config.command_help("leave"))
    async def leave(self, ctx):
        await ctx.music_service.leave()


    @commands.command(help=config.command_help("lyrics"))
    async def lyrics(self, ctx):
        lyrics = ctx.music_service.current_lyrics()
        lines = lyrics.splitlines()
        line_groups = self.group_elements(lines, 70)
        pages = [ utils.embedded_message(message="\n".join(group)) for group in line_groups ]
        await self.show_pages(ctx, pages=pages)


    @play.before_invoke
    @skip.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    @shuffle.before_invoke
    async def check_voice_connection(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise exceptions.UserNotConnectedToVoiceChannel()

        if ctx.voice_client and ctx.voice_client.channel != ctx.author.voice.channel:
            raise exceptions.BotIsConnectedToAnotherChanel()


    @shuffle.after_invoke
    @leave.after_invoke
    async def add_ok_reaction(self, ctx):
        await ctx.message.add_reaction(self.OK_EMOJI)


    def get_music_service(self, ctx):
        service = self.services.get(ctx.guild.id, None)
        if not service:
            service = MusicService(self.bot)
            self.services[ctx.guild.id] = service

        return service

    def group_elements(self, elements, group_size):
        return [ elements[i:i+group_size] for i in range(0, len(elements), group_size) ]


    # Discord Cog #

    #def cog_unload(self):
    #    for service in self.services.values():
    #        self.bot.loop.create_task(service.finish())

    def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage("This command can\'t be used in DM channels")
        return True

    async def cog_before_invoke(self, ctx):
        ctx.music_service = self.get_music_service(ctx)



def setup(bot):
    bot.add_cog(MusicCog(bot))