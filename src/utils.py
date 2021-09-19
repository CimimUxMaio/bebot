from typing import Union
import discord


def bold(text):
    return f"**{text}**" if text else ""

def italics(text):
    return f"*{text}*" if text else ""


def embedded_message(*, event=None, message, color=discord.Colour.blue(), blame: Union[discord.User, discord.Member] = None):
    premessage = bold(event + ': ') if event else ""
    complete_message = premessage + message
    embed = discord.Embed(description=complete_message, color=color) 

    if blame:
        embed.set_footer(icon_url=blame.avatar_url, text=blame.display_name)
        
    return embed