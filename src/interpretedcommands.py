from datetime import datetime
from exceptions import MissingParameter
import guildmanager

async def ping(ctx, *args):
    latency = (datetime.utcnow() - ctx.message.created_at).total_seconds() * 1000
    await ctx.send(f"Pong! Latency: {latency} ms")


async def time(ctx, *args):
    await ctx.send(f"Time: {datetime.now()}")


async def play(ctx, *args):
    if len(args) == 0:
        raise MissingParameter("song_name")

    song_name = ' '.join(args)
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.play(ctx, song_name=song_name)


COMMAND_MAPPINGS = {
    0: ping,
    1: time,
    2: play
}