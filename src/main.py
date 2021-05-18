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



PREFIX = config.BOT_PREFIX
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command("help")


# MANUAL COMMANDS #

@bot.command(aliases=["h"], description="Shows this message")
async def help(ctx):
    embed = discord.Embed(title="Help", color = discord.Colour.blue())

    SEPARATOR = "\u200b"

    embed.add_field(name="INTERPRETED", value="The command can be interpreted by a given sentence. Command parameters must be given between '[]'", inline=False)
    for name, info in config.interpreted_commands().items():
        command_namings = f"**{name}**"
        command_parameters = ' '.join([f"<{param_name}>" for param_name in info["parameters"]])
        command_description = info["description"]
        field_title = '  '.join([command_namings, command_parameters])
        embed.add_field(name=field_title, value=command_description, inline=False)  # Will fail if description is BLANK

    embed.add_field(name=SEPARATOR, value=SEPARATOR, inline=False)
    embed.add_field(name="MANUAL", value="The exact command name or alias should be passed for the command to work", inline=False)
    for cmd in bot.commands:
        command_namings = f"**{cmd.name}**" + "".join([f" | {alias}" for alias in cmd.aliases])
        command_parameters = ' '.join([f"<{param_name}>" for param_name in cmd.clean_params.keys()])
        command_description = cmd.description
        field_title = '  '.join([command_namings, command_parameters])
        embed.add_field(name=field_title, value=command_description, inline=False)  # Will fail if description is BLANK
        
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


@bot.command(aliases=["cl"], description=config.description("classify_last"))
async def classify_last(ctx, classification):
    datacollector.check_classification(bot, classification)
    classified_message = datacollector.classify_last_uninterpreted_message(classification)
    await ctx.send(f"\"{classified_message}\" classified as \"{classification}\"")


@bot.command(description=config.description("skip"))
async def skip(ctx):
    await musicservice.INSTANCE.skip(ctx)


# EVENTS #

def is_manual_command(command_name):
    manual_commands = itertools.chain(*[[command.name] + command.aliases for command in bot.commands])
    return command_name in manual_commands


@bot.event
async def on_command_error(ctx, error):
    if hasattr(error, "original"):
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