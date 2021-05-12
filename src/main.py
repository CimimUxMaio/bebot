from discord.ext import commands
from discord.ext.commands.errors import CommandError, MissingRequiredArgument
from discord.ext.commands.help import DefaultHelpCommand
from brain import BRAIN
import config
from exceptions import ModelException
import parsing
import datacollector
import itertools
import interpretedcommands as icommands



PREFIX = config.BOT_PREFIX
bot = commands.Bot(command_prefix=PREFIX, help_command=DefaultHelpCommand())



# INTERPRETED COMMANDS #

@bot.command(brief=config.brief("ping"), description=config.description("ping"))
async def ping(ctx):
    await icommands.ping(ctx)


@bot.command(aliases=["p"], brief=config.brief("play"), description=config.description("play"))
async def play(ctx, *, song_name):
    await icommands.play(ctx, song_name)


@bot.command(brief=config.brief("time"), description=config.description("time"))
async def time(ctx):
    await icommands.time(ctx)



# STRICTLY MANUAL COMMANDS #

@bot.command(aliases=["cl"], brief=config.brief("classify_last"), description=config.description("classify_last"))
async def classify_last(ctx, classification):
    datacollector.check_classification(bot, classification)
    classified_message = datacollector.classify_last_uninterpreted_message(classification)
    await ctx.send(f"\"{classified_message}\" classified as \"{classification}\"")


# EVENTS #

def is_manual_command(command_name):
    manual_commands = itertools.chain(*[[command.name] + command.aliases for command in bot.commands])
    return command_name in manual_commands

async def handle_model_error(ctx, error):
    await ctx.send(str(error))


@bot.event
async def on_command_error(ctx, error):
    if hasattr(error, "original") and isinstance(error.original, ModelException):
        await handle_model_error(ctx, error.original)
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

    first_word = without_prefix.split()[0]
    if is_manual_command(first_word):
        await bot.process_commands(message)
        return

    command_message, parameters = parsing.parse_message(without_prefix)
    command = BRAIN.identify_command(command_message)
    ctx = await bot.get_context(message)
    try:
        await command(ctx, *parameters)
    except ModelException as error:
        await handle_model_error(ctx, error)


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)