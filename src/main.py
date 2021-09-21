import discord
from discord.ext import commands
import config
import utils
import cogs.MusicCog as musiccog
import cogs.HelpCog as helpcog
import cogs.MiscellaneousCog as miscellaneouscog


PREFIX = config.BOT_PREFIX
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command("help")


# SETUP #

musiccog.setup(bot)
miscellaneouscog.setup(bot)
helpcog.setup(bot)


# EVENTS #

@bot.event
async def on_ready():
    print("Bot ready!")


@bot.event
async def on_command_error(ctx, error):
    original_error = error
    if hasattr(error, "original"):
        original_error = error.original
    
    if isinstance(original_error, commands.CommandError):
        embed = utils.embedded_message(event="Error", message=str(error), color=discord.Colour.red())
        await utils.send_temporary_embed(ctx, embed=embed)
        return

    raise error


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)