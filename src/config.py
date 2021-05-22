import json
import enum


with open("../private_config.json", "r") as private_config_file:
    PRIVATE_CONFIG = json.load(private_config_file)

BOT_TOKEN = PRIVATE_CONFIG["botToken"]


with open("../bot_config.json", "r") as bot_config_file:
    BOT_CONFIG = json.load(bot_config_file)

BOT_PREFIX = BOT_CONFIG["prefix"]


with open("../command_config.json", "r") as command_config_file:
    COMMAND_CONFIG = json.load(command_config_file)

def category_description(category):
    return COMMAND_CONFIG["categories"][category]

def command_info(command_name):
    return COMMAND_CONFIG["commands"][command_name]


with open("../brain_config.json", "r") as brain_config_file:
    BRAIN_CONFIG = json.load(brain_config_file)

MIN_CONFIDENCE = BRAIN_CONFIG["minConfidence"]
COMMAND_MAPPINGS = { int(k): cmd_name for k, cmd_name in BRAIN_CONFIG["commandMappings"].items() }