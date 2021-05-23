import discord


async def send_embeded_message(ctx, *, action=None, message, color=discord.Colour.blue(), blame: discord.Member=None):
    premessage = f"**{action}:** " if action else ""
    complete_message = premessage + message
    embed = discord.Embed(description=complete_message, color=color) 

    if blame:
        embed.set_footer(icon_url=ctx.author.avatar_url, text=blame.display_name)
        
    await ctx.send(embed=embed)