from discord.ext import commands
from discord.ext.commands.errors import CommandError, MissingRequiredArgument
from discord.ext.commands.help import DefaultHelpCommand
from brain import BRAIN
import config
from exceptions import ModelException, UnknownCommand
import parsing
import datacollector
import itertools
from datetime import datetime


PREFIX = config.BOT_PREFIX
bot = commands.Bot(command_prefix=PREFIX, help_command=DefaultHelpCommand())


# INTERPRETED COMMANDS #

@bot.command(brief=config.brief("ping"), description=config.description("ping"))
async def ping(ctx, *args):
    latency = (datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000
    await ctx.send(f"Pong! Latency: {latency} ms")


@bot.command(aliases=["p"], brief=config.brief("play"), description=config.description("play"))
async def play(ctx, song, *args):
    await ctx.send(f"Playing \"{' '.join([song] + [*args])}\"")


@bot.command(brief=config.brief("time"), description=config.description("time"))
async def time(ctx, *args):
    await ctx.send(f"Time: {datetime.now()}")


# MANUAL COMMANDS #

@bot.command(aliases=["cl"], brief=config.brief("classify_last"), description=config.description("classify_last"))
async def classify_last(ctx, classification):
    datacollector.check_classification(bot, classification)
    classified_message = datacollector.classify_last_uninterpreted_message(classification)
    await ctx.send(f"\"{classified_message}\" classified as \"{classification}\"")


# EVENTS #

@bot.event
async def on_command_error(ctx, error):
    if hasattr(error, "original"):
        if isinstance(error.original, ModelException):
            if isinstance(error.original, UnknownCommand):
                datacollector.set_last_uninterpreted_message(error.original.command_message)
                return
            
        await ctx.send(str(error.original))
        return
    elif isinstance(error, CommandError):
        await ctx.send(str(error))
        return

    raise error


@bot.event
async def on_ready():
    print("Bot ready!")


@bot.event
async def on_message(message):
    if not message.content.startswith(PREFIX):
        return

    without_prefix = message.content.lstrip(PREFIX)

    if len(without_prefix) == 0:
        return

    predefined_commands = itertools.chain(*[[command.name] + command.aliases for command in bot.commands])
    first_word = without_prefix.split()[0]
    if first_word in predefined_commands:
        await bot.process_commands(message)
    else:
        command_message, parameters = parsing.parse_message(without_prefix)
        command_name = BRAIN.identify_command(command_message)
        ctx = await bot.get_context(message)
        await ctx.invoke(bot.get_command(command_name), *parameters)
     

if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)