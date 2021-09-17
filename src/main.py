from inspect import signature
import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandError
import config
from exceptions import ModelException
import utils
import guildmanager


PREFIX = config.BOT_PREFIX
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command("help")


# COMMANDS #

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
    

@bot.command(aliases=["s"], help=config.command_help("skip"))
async def skip(ctx, position: int = 1):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.skip(ctx, position-1)


@bot.command(aliases=["q"], help=config.command_help("queue"))
async def queue(ctx):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.show_queue(ctx)


@bot.command(aliases=["p"], help=config.command_help("play"))
async def play(ctx, *, search_string):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.play(ctx, search_string=search_string)


# EVENTS #

async def handle_error(ctx, error):
    embed = utils.embeded_message(event="Error", message=str(error), color=discord.Colour.red())
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    original_error = error

    if hasattr(error, "original"):
        original_error = error.original
        
    if isinstance(original_error, ModelException) or isinstance(original_error, CommandError):
        await handle_error(ctx, original_error)
        return

    raise error


@bot.event
async def on_ready():
    for guild in bot.guilds:
        guildmanager.register(guild_id=guild.id)

    print("Bot ready!")


@bot.event
async def on_guild_join(guild):
    guildmanager.register(guild_id=guild.id)
    

@bot.event
async def on_message(message):
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)