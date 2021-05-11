import json

from discord.ext import commands


with open("../bot_config.json", "r") as bot_config_file:
    BOT_CONFIG = json.load(bot_config_file)


BOT_TOKEN = BOT_CONFIG["botToken"]
BOT_PREFIX = BOT_CONFIG["prefix"]


with open("../command_config.json", "r") as command_config_file:
    COMMAND_CONFIG = json.load(command_config_file)


def description(command_name):
    return f'({COMMAND_CONFIG[command_name]["type"]}) {COMMAND_CONFIG[command_name]["description"]}'

def brief(command_name):
    return COMMAND_CONFIG[command_name]["brief"]