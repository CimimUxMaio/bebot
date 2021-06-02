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
from commandmanager import INSTANCE as icmd_manager


PREFIX = config.BOT_PREFIX
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command("help")


# MANUAL COMMANDS #

@bot.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(title="Help", color = discord.Colour.blue())

    SEPARATOR = "\u200b"

    embed.add_field(name="__Manual__", value=f"_{config.category_description('manual')}_", inline=False)
    for manual_cmd in bot.commands:
        aliases = manual_cmd.aliases
        info = config.command_info(manual_cmd.name)
        command_namings = f"**{manual_cmd.name} { '|' if aliases else ''} {' | '.join(aliases)}**"
        command_parameters = ' '.join([f"<{param_name}>" for param_name in info["parameters"]])
        command_description = info["description"]
        field_title = '  '.join([command_namings, command_parameters])
        embed.add_field(name=field_title, value=command_description, inline=False)  # Will fail if description is BLANK

    embed.add_field(name=SEPARATOR, value=SEPARATOR, inline=False)
    embed.add_field(name="__Interpreted__", value=f"_{config.category_description('interpreted')}_", inline=False)
    for command in icmd_manager.commands.values():
        embed.add_field(name=command.shape_description_formated, value=command.description, inline=False)  # Will fail if description is BLANK

    await ctx.send(embed=embed)


@bot.command(aliases=["tl"])
async def teach_last(ctx, classification):
    classified_message = datacollector.classify_last_message(classification)
    await ctx.send(f"\"{classified_message}\" classified as \"{classification}\"")


# INTERPRETED COMMANDS #

@icmd_manager.icommand(**config.command_info("skip"))
async def skip(ctx, song_index=1):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.skip(ctx, int(song_index)-1)


@icmd_manager.icommand(**config.command_info("queue"))
async def queue(ctx):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.show_queue(ctx)


@icmd_manager.icommand(**config.command_info("play"))
async def play(ctx, *args):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.play(ctx, song_names=args)


# EVENTS #

def is_manual_command(command_name):
    manual_commands = itertools.chain(*[[command.name] + command.aliases for command in bot.commands])
    return command_name in manual_commands


async def handle_error(ctx, error):
    await utils.send_embeded_message(ctx, action="Error", message=str(error), color=discord.Colour.red())


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
        cmd_name = BRAIN.identify_command(command_message)
        await icmd_manager[cmd_name](ctx, *parameters)
    except ModelException as error:
        await handle_error(ctx, error)


if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)