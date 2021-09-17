import json
import os
import dotenv

dotenv.load_dotenv()


BOT_TOKEN = os.getenv("TOKEN")
BOT_PREFIX = os.getenv("PREFIX")


with open("./commands.config.json", "r") as command_config_file:
    COMMAND_CONFIG = json.load(command_config_file)

def command_help(command):
    return COMMAND_CONFIG[command]["help"]