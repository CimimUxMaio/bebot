from cogs.BaseCog import BaseCog
from discord.ext.commands import command
import random
import utils
import config


dice_emojis = {
    1: u"\u2680",
    2: u"\u2681",
    3: u"\u2682",
    4: u"\u2683",
    5: u"\u2684",
    6: u"\u2685"
}

class MiscellaneousCog(BaseCog, name="Miscellaneous"):
    @command(help=config.command_help("dices"))
    async def dices(self, ctx):
        result = random.randint(1, 6)
        await ctx.send(embed=utils.embedded_message(
            message=f"{result} {dice_emojis[result]}"
        ))



def setup(bot):
    bot.add_cog(MiscellaneousCog(bot))