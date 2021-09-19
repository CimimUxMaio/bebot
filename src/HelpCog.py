import asyncio
import discord
from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog
import config
import discord.ext.commands as commands
from discord import Embed, Colour
import utils


class HelpCog(Cog, name="Help"):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.command(aliases=["h"], help=config.command_help("help"))
    async def help(self, ctx: commands.Context):
        prefix = await self.bot.get_prefix(ctx)
        cogs = self.bot.cogs.values()
        page_amount = len(cogs)
        pages = [ self.cog_description(prefix, page_amount, n, cog) for n, cog in enumerate(cogs, start=1) ]
        
        cur_page = 0
        message: discord.Message = await ctx.send(embed=pages[cur_page])

        BACKWARD_EMOJI = u"\u25c0"
        FORWARD_EMOJI = u"\u25b6"

        await message.add_reaction(BACKWARD_EMOJI)
        await message.add_reaction(FORWARD_EMOJI)

        def check(reaction: discord.Reaction, user):
            return reaction.message == message and user == ctx.author and str(reaction.emoji) in [BACKWARD_EMOJI, FORWARD_EMOJI]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
                if str(reaction.emoji) == FORWARD_EMOJI and cur_page != len(pages) -1:
                    cur_page += 1
                    await message.edit(embed=pages[cur_page])
                elif str(reaction.emoji) == BACKWARD_EMOJI and cur_page > 0:
                    cur_page -= 1
                    await message.edit(embed=pages[cur_page])
                
                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await message.delete()
                return


    def command_description(self, prefix, cmd):
        params = cmd.signature
        return utils.bold(f"{prefix} {cmd.name}") + f" {utils.italics(params)}\n{cmd.help}"
    

    def cog_description(self, prefix, page_amount, n, cog: Cog):
        description="\n\n".join([ self.command_description(prefix, cmd) for cmd in cog.get_commands() ])
        embed = Embed(
            title=cog.qualified_name,
            description=description,
            color=Colour.blue()
        )

        embed.set_footer(text=f"Page {n}/{page_amount}")
        return embed
    


def setup(bot):
    bot.add_cog(HelpCog(bot))