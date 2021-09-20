import asyncio
from typing import Union
from async_timeout import timeout
import discord
from discord.ext.commands import Context


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


async def send_temporary_embed(ctx: Context, *, embed: discord.Embed, duration=5):
    message: discord.Message = await ctx.send(embed=embed)
    await asyncio.sleep(duration)
    await message.delete()