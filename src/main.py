import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandError
from brain import BRAIN
import config
from exceptions import ModelException
import parsing
import datacollector
import itertools
import utils
import guildmanager



PREFIX = config.BOT_PREFIX
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command("help")


# MANUAL COMMANDS #

@bot.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(title="Help", color = discord.Colour.blue())

    SEPARATOR = "\u200b"

    last_category = len(config.CommandCategory) - 1 
    for n, category in enumerate(config.CommandCategory):
        embed.add_field(name=f"__{category.value}:__", value=f"_{config.category_description(category)}_", inline=False)
        for command in config.commands(category):
            manual_cmd = bot.get_command(command["name"])
            aliases = manual_cmd.aliases if manual_cmd else []
            command_namings = f"**{command['name']} { '|' if aliases else ''} {' | '.join(aliases)}**"
            command_parameters = ' '.join([f"<{param_name}>" for param_name in command["parameters"]])
            command_description = command["description"]
            field_title = '  '.join([command_namings, command_parameters])
            embed.add_field(name=field_title, value=command_description, inline=False)  # Will fail if description is BLANK
        
        if n != last_category:
            embed.add_field(name=SEPARATOR, value=SEPARATOR, inline=False)

    await ctx.send(embed=embed)


@bot.command(aliases=["tl"])
async def teach_last(ctx, classification):
    classified_message = datacollector.classify_last_message(classification)
    await ctx.send(f"\"{classified_message}\" classified as \"{classification}\"")


@bot.command()
async def skip(ctx):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.skip(ctx)

@bot.command(aliases=["q"])
async def queue(ctx):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.queued_songs(ctx)


# EVENTS #

def is_manual_command(command_name):
    manual_commands = itertools.chain(*[[command.name] + command.aliases for command in bot.commands])
    return command_name in manual_commands


async def handle_error(ctx, error):
    await utils.embeded_message(ctx, action="Error", message=str(error), color=discord.Colour.red())


@bot.event
async def on_command_error(ctx, error):
    original_error = error

    if hasattr(error, "original"):
        original_error = error.original
        
    if isinstance(original_error, ModelException) or isinstance(original_error, CommandError):
        handle_error(ctx, original_error)
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
    ctx = await bot.get_context(message)
    try:
        command = BRAIN.identify_command(command_message)
        await command(ctx, *parameters)
    except ModelException as error:
        await handle_error(ctx, error)


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)