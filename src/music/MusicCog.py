from discord.colour import Colour
from discord.ext.commands.cog import Cog
import exceptions
from discord.ext import commands
import config
from music.MusicService import MusicService
from music.Song import Song
import utils


class MusicCog(Cog, name="Music"):
    def __init__(self, bot):
        self.bot = bot
        self.services = {}
    
    @commands.command(aliases=["s"], help=config.command_help("skip"))
    async def skip(self, ctx, position: int = 0):
        if not ctx.music_service.is_playing:
            raise exceptions.NothingIsCurrentlyPlaying()

        await ctx.message.add_reaction(u"\U0001F44C")
        skipped = ctx.music_service.skip(position)
        await ctx.send(embed=utils.embedded_message(
            event="Skipped",
            message=skipped.description,
            blame=ctx.author
        ))
    
    
    @commands.command(aliases=["q"], help=config.command_help("queue"))
    async def queue(self, ctx):
        message = "Queue is empty"
        if ctx.music_service.current:
            message = utils.bold(f"Current: {ctx.music_service.current.description}") + "\n"
            queue = ctx.music_service.queue
            queued = [ f"{pos}. {song.description}" for pos, song in enumerate(queue, start=1) ]
            message += "\n".join(queued)

        await ctx.send(embed=utils.embedded_message(
            message=message
        ))

    
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


    @play.before_invoke
    @skip.before_invoke
    async def check_voice_conection(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise exceptions.UserNotConnectedToVoiceChannel()

        if ctx.voice_client and ctx.voice_client.channel != ctx.author.voice.channel:
            raise exceptions.BotIsConnectedToAnotherChanel()


    def get_music_service(self, ctx):
        service = self.services.get(ctx.guild.id, None)
        if not service:
            service = MusicService(self.bot)
            self.services[ctx.guild.id] = service

        return service


    # Discord Cog #

    def cog_unload(self):
        for service in self.services.values():
            self.bot.loop.create_task(service.finish())

    def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage("This command can\'t be used in DM channels")
        return True

    async def cog_before_invoke(self, ctx):
        ctx.music_service = self.get_music_service(ctx)


def setup(bot):
    bot.add_cog(MusicCog(bot))