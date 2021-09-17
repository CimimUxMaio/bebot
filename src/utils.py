from collections import namedtuple
import discord


def bold(text):
    return f"**{text}**" if text else ""

def italics(text):
    return f"*{text}*" if text else ""


class Blamed:
    def __init__(self, member: discord.Member):
        self._display_name = member.display_name
        self._avatar_url = member.avatar_url
    
    @property
    def display_name(self):
        return self._display_name

    @property
    def avatar_url(self):
        return self._avatar_url


def embeded_message(*, action=None, message, color=discord.Colour.blue(), blame: Blamed = None):
    premessage = bold(action + ': ') if action else ""
    complete_message = premessage + message
    embed = discord.Embed(description=complete_message, color=color) 

    if blame:
        embed.set_footer(icon_url=blame.avatar_url, text=blame.display_name)
        
    return embed