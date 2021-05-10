from datetime import datetime

async def unknown(ctx, *args):
    await ctx.send("Unknown command")


async def ping(ctx, *args):
    await ctx.send("Pong!")


async def play(ctx, *args):
    await ctx.send(f"Playing \"{' '.join(args)}\"")


async def time(ctx, *args):
    await ctx.send(f"Time: {datetime.now()}")



COMMAND_MAPPINGS = {
    0: ping,
    1: time,
    2: play
}