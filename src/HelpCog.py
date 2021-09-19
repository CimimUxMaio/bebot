import asyncio
import discord
from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog
from BaseCog import BaseCog
import config
import discord.ext.commands as commands
from discord import Embed, Colour
import utils


class HelpCog(BaseCog, name="Help"):
    @commands.command(aliases=["h"], help=config.command_help("help"))
    async def help(self, ctx: commands.Context):
        prefix = await self.bot.get_prefix(ctx)
        cogs = self.bot.cogs.values()
        pages = [ self.cog_description(prefix, cog) for cog in cogs ]
        await self.show_pages(ctx, pages=pages)


    def command_description(self, prefix, cmd):
        params = cmd.signature
        return utils.bold(f"{prefix} {cmd.name}") + f" {utils.italics(params)}\n{cmd.help}"
    

    def cog_description(self, prefix, cog: Cog):
        description="\n\n".join([ self.command_description(prefix, cmd) for cmd in cog.get_commands() ])
        return Embed(
            title=cog.qualified_name,
            description=description,
            color=Colour.blue()
        )



def setup(bot):
    bot.add_cog(HelpCog(bot))