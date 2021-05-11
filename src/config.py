import json


with open("../bot_config.json", "r") as bot_config_file:
    BOT_CONFIG = json.load(bot_config_file)


BOT_TOKEN = BOT_CONFIG["botToken"]
BOT_PREFIX = BOT_CONFIG["prefix"]


with open("../command_config.json", "r") as command_config_file:
    COMMAND_CONFIG = json.load(command_config_file)