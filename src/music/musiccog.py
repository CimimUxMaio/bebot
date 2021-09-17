from discord.ext import commands
import guildmanager
import config


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["s"], help=config.command_help("skip"))
    async def skip(self, ctx, position: int = 1):
        musicservice = self.get_music_service(ctx)
        await musicservice.skip(ctx, position-1)
    
    
    @commands.command(aliases=["q"], help=config.command_help("queue"))
    async def queue(self, ctx):
        musicservice = self.get_music_service(ctx)
        await musicservice.show_queue(ctx)
    
    
    @commands.command(aliases=["p"], help=config.command_help("play"))
    async def play(self, ctx, *, search_string):
        musicservice = self.get_music_service(ctx)
        await musicservice.play(ctx, search_string=search_string)


    def get_music_service(self, ctx):
        return guildmanager.get_state(ctx.guild.id).music_service



def setup(bot):
    bot.add_cog(MusicCog(bot))