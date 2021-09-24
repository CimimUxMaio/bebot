from discord.embeds import Embed
from discord.channel import TextChannel
from discord.ext.commands.bot import Bot
from discord.utils import get
import dotenv
import os
import json


dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")

with open("./notifications/message.json", "r") as file:
    MESSAGE_JSON = json.load(file)

MESSAGE = Embed(
    title=MESSAGE_JSON["title"],
    description=MESSAGE_JSON["description"]
)

for item in MESSAGE_JSON["items"]:
    MESSAGE.add_field(name=item["name"], value=item["value"])


bot = Bot(command_prefix=None)
bot.recursively_remove_all_commands()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        notif_channel: TextChannel = get(guild.text_channels, name="bebot-notifications")

        if notif_channel:
            await notif_channel.send(embed=MESSAGE)

    await bot.close()



if __name__ == "__main__":
    bot.run(TOKEN)