import json
import os
import dotenv

dotenv.load_dotenv()


BOT_TOKEN = os.getenv("TOKEN")
BOT_PREFIX = os.getenv("PREFIX")


with open("./command_config.json", "r") as command_config_file:
    COMMAND_CONFIG = json.load(command_config_file)

def category_description(category):
    return COMMAND_CONFIG["categories"][category]

def command_info(command_name):
    return COMMAND_CONFIG["commands"][command_name]

PARAM_WRAPPERS = COMMAND_CONFIG["paramWrappers"]