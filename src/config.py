import json
import enum
from token import COMMA


with open("../bot_config.json", "r") as bot_config_file:
    BOT_CONFIG = json.load(bot_config_file)


BOT_TOKEN = BOT_CONFIG["botToken"]
BOT_PREFIX = BOT_CONFIG["prefix"]


with open("../command_config.json", "r") as command_config_file:
    COMMAND_CONFIG = json.load(command_config_file)


class CommandCategory(enum.Enum):
    MANUAL = "Manual"
    INTERPRETED = "Interpreted"


def category_description(category: CommandCategory):
    return COMMAND_CONFIG[category.value]["description"]

def commands(category: CommandCategory):
    return [ cmd for cmd in COMMAND_CONFIG[category.value]["commands"] ]

def interpreted_commands():
    return commands(CommandCategory.INTERPRETED)

def manual_commands():
    return commands(CommandCategory.MANUAL)
