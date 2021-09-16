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


# MANUAL COMMANDS #

def command_formated_description(command_name):
    cmd_info = config.command_info(command_name)
    cmd_name = f"**{command_name}**"
    cmd_parameters = ' '.join([f"<{param_name}>" for param_name in cmd_info["parameters"]])
    cmd_optionals = ' '.join([f"<{optional_name}, default={default}>" for optional_name, default in cmd_info["optionals"]])

    description = cmd_info["description"]
    title = '  '.join([cmd_name, cmd_parameters, cmd_optionals])
    return title, description


def command_category_embed(*, category_name, command_names):
    embed = discord.Embed(title=category_name, description=f"_{config.category_description(category_name.lower())}_", color = discord.Colour.blue())
    for cmd in command_names:
        title, description = command_formated_description(cmd)
        embed.add_field(name=title, value=description, inline=False)

    return embed

@bot.command(aliases=["h"])
async def help(ctx):
    await ctx.send(embed=command_category_embed(
        category_name="Manual",
        command_names=[cmd.name for cmd in bot.commands]
    ))
    

# INTERPRETED COMMANDS #

@bot.command(aliases=["s"])
async def skip(ctx, song_index=1):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.skip(ctx, int(song_index)-1)


@bot.command(aliases=["q"])
async def queue(ctx):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.show_queue(ctx)


@bot.command(aliases=["p"])
async def play(ctx, *args):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.play(ctx, song_name=" ".join(args))


# EVENTS #

async def handle_error(ctx, error):
    await utils.send_embeded_message(ctx, action="Error", message=str(error), color=discord.Colour.red())


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