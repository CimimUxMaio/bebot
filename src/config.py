import json


with open("../config.json", "r") as config_file:
    CONFIG = json.load(config_file)


BOT_TOKEN = CONFIG["botToken"]
PREFIX = CONFIG["prefix"]