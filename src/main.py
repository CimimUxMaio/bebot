from discord.ext import commands
from brain import BRAIN
import config
import parsing


PREFIX = config.PREFIX
bot = commands.Bot(command_prefix=PREFIX)


@bot.event
async def on_ready():
    print("Bot ready!")


@bot.event
async def on_message(message):
    if not message.content.startswith(PREFIX):
        return

    ctx = await bot.get_context(message)

    without_prefix = message.content.lstrip(PREFIX)
    command_message, parameters = parsing.parse_message(without_prefix)
    await BRAIN.identify_command(command_message)(ctx, *parameters)
     

if __name__ == "__main__":
    bot.run(config.BOT_TOKEN)