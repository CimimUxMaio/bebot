import asyncio
import discord
from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog

class BaseCog(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

        self.BACKWARD_EMOJI = u"\u25c0"
        self.FORWARD_EMOJI = u"\u25b6"

    async def show_pages(self, ctx, *, pages, timeout=30):
        # page amount must be at least 1 
        page_amount = len(pages)
        numerated_pages = [ p.set_footer(text=f"Page {n}/{page_amount}") for n, p in enumerate(pages, start=1) ]
        cur_page = 0
        message: discord.Message = await ctx.send(embed=numerated_pages[cur_page])

        await message.add_reaction(self.BACKWARD_EMOJI)
        await message.add_reaction(self.FORWARD_EMOJI)

        def check(reaction: discord.Reaction, user):
            return reaction.message == message and user == ctx.author and str(reaction.emoji) in [self.BACKWARD_EMOJI, self.FORWARD_EMOJI]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=timeout)
                if str(reaction.emoji) == self.FORWARD_EMOJI:
                    cur_page = min(cur_page+1, page_amount-1)
                elif str(reaction.emoji) == self.BACKWARD_EMOJI:
                    cur_page = max(cur_page-1, 0)
                
                await message.edit(embed=numerated_pages[cur_page])
                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await message.delete()
                return