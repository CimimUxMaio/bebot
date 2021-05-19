import discord


async def embeded_message(ctx, *, action=None, message, color=discord.Colour.blue(), blame: discord.Member=None):
    premessage = f"**{action}:** " if action else ""
    complete_message = premessage + message
    embed = discord.Embed(description=complete_message, color=color) 

    if blame:
        embed.set_footer(blame.mention)
        
    await ctx.send(embed=embed)