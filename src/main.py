import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandError
from brain import BRAIN
import config
from exceptions import ModelException, handle_model_error
import parsing
import datacollector
import itertools
import musicservice
import utils



PREFIX = config.BOT_PREFIX
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command("help")


# MANUAL COMMANDS #

@bot.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(title="Help", color = discord.Colour.blue())

    SEPARATOR = "\u200b"

    for category in config.CommandCategory:
        embed.add_field(name=category.value, value=config.category_description(category), inline=False)
        for command in config.commands(category):
            command_namings = f"**{command['name']}**"
            command_parameters = ' '.join([f"<{param_name}>" for param_name in command["parameters"]])
            command_description = command["description"]
            field_title = '  '.join([command_namings, command_parameters])
            embed.add_field(name=field_title, value=command_description, inline=False)  # Will fail if description is BLANK
        embed.add_field(name=SEPARATOR, value=SEPARATOR, inline=False)

    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


@bot.command(aliases=["tl"])
async def teach_last(ctx, classification):
    classified_message = datacollector.classify_last_message(classification)
    await ctx.send(f"\"{classified_message}\" classified as \"{classification}\"")


@bot.command()
async def skip(ctx):
    await musicservice.INSTANCE.skip(ctx)


# EVENTS #

def is_manual_command(command_name):
    manual_commands = itertools.chain(*[[command.name] + command.aliases for command in bot.commands])
    return command_name in manual_commands


@bot.event
async def on_command_error(ctx, error):
    original_error = error

    if hasattr(error, "original"):
        original_error = error.original
        
    if isinstance(original_error, ModelException) or isinstance(original_error, CommandError):
        utils.embeded_message(ctx, action="Error", message=str(original_error), color=discord.Colour.red())
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
    datacollector.set_last_message(command_message)
    command = BRAIN.identify_command(command_message)
    ctx = await bot.get_context(message)
    try:
        await command(ctx, *parameters)
    except ModelException as error:
        await handle_model_error(ctx, error)


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)