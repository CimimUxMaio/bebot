from datetime import datetime
from exceptions import MissingParameter
import musicservice


async def ping(ctx, *args):
    latency = (datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000
    await ctx.send(f"Pong! Latency: {latency} ms")


async def time(ctx, *args):
    await ctx.send(f"Time: {datetime.now()}")


async def play(ctx, *args):
    if len(args) == 0:
        raise MissingParameter("song_name")

    song_name = ' '.join(args)
    await musicservice.INSTANCE.play(ctx, song_name=song_name)