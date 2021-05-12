from datetime import datetime
import datacollector
from exceptions import MissingParameter


async def undefined(command_message):
    async def f(ctx, *args):
        datacollector.set_last_uninterpreted_message(command_message)
        await ctx.send(f"Couldn't resolve \"{command_message}\" to a valid command")

    return f


async def ping(ctx, *args):
    latency = (datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000
    await ctx.send(f"Pong! Latency: {latency} ms")


async def play(ctx, *args):
    if len(args) == 0:
        raise MissingParameter("song_name")

    await ctx.send(f"Playing \"{' '.join(args)}\"")


async def time(ctx, *args):
    await ctx.send(f"Time: {datetime.now()}")