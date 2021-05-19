import discord


async def embeded_message(ctx, *, action=None, message, color=discord.Colour.blue()):
    premessage = f"**{action}:** " if action else ""
    complete_message = premessage + message
    embed = discord.Embed(description=complete_message) 
    await ctx.send(embed=embed)