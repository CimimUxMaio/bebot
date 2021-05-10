from datetime import datetime


async def unknown(client, message, *args):
    ctx = await client.get_context(message)
    await ctx.send("Unknown command")


async def ping(client, message, *args):
    ctx = await client.get_context(message)
    latency = (datetime.utcnow() - message.created_at).total_seconds() * 1000
    await ctx.send(f"Pong! Latency: {latency} ms")


async def play(client, message, *args):
    ctx = await client.get_context(message)
    await ctx.send(f"Playing \"{' '.join(args)}\"")


async def time(client, message, *args):
    ctx = await client.get_context(message)
    await ctx.send(f"Time: {datetime.now()}")


COMMAND_MAPPINGS = {
    0: ping,
    1: time,
    2: play
}