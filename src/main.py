from discord.ext import commands
from discord.ext.commands.help import DefaultHelpCommand
from brain import BRAIN
import config
import parsing
import datacollector
import itertools
from datetime import datetime


PREFIX = config.PREFIX
bot = commands.Bot(command_prefix=PREFIX, help_command=DefaultHelpCommand())


# INTERPRETED COMMANDS #

@bot.command()
async def ping(ctx, *args):
    latency = (datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000
    await ctx.send(f"Pong! Latency: {latency} ms")


@bot.command(aliases=["p"])
async def play(ctx, *args):
    await ctx.send(f"Playing \"{' '.join(args)}\"")


@bot.command()
async def time(ctx, *args):
    await ctx.send(f"Time: {datetime.now()}")


# MANUAL COMMANDS #

@bot.command(aliases=["cl"])
async def classify_last(ctx, classification):
    datacollector.check_classification(client, classification)
    classified_message = datacollector.classify_last_command_message(classification)
    await ctx.send(f"\"{classified_message}\" classified as \"{classification}\"")


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
        datacollector.set_last_command_message(command_message)
        command_name = BRAIN.identify_command(command_message)
        ctx = await bot.get_context(message)
        await ctx.invoke(bot.get_command(command_name), *parameters)
     

if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)