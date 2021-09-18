from discord.ext.commands.cog import Cog
from discord.ext.commands.errors import CommandError
import utils
from discord import Colour

class BaseCog(Cog):
    async def cog_command_error(self, ctx, error):
        original_error = error
        if hasattr(error, "original"):
            original_error = error.original

        if isinstance(original_error, CommandError):
            embed = utils.embedded_message(event="Error", message=str(error), color=Colour.red())
            await ctx.send(embed=embed)
            return

        raise error