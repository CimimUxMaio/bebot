import discord
from discord.ext import commands
import config
import utils
import music.MusicCog as musiccog


PREFIX = config.BOT_PREFIX
bot = commands.Bot(command_prefix=PREFIX)

bot.remove_command("help")

musiccog.setup(bot)



@bot.command(aliases=["h"], help=config.command_help("help"))
async def help(ctx):
    def command_description(cmd):
        params = cmd.signature
        return utils.bold(f"{PREFIX} {cmd.name}") + f" {utils.italics(params)}\n{cmd.help}"

    description="\n\n".join([ command_description(cmd) for cmd in bot.commands ])
    embed = discord.Embed(
        title="Help",
        description=description,
        color=discord.Colour.blue()
    )
    await ctx.send(embed=embed)



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
        await ctx.send(embed=embed)
        return

    raise error


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)