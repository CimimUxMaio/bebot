from exceptions import MissingParameter
import guildmanager


async def skip(ctx):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.skip(ctx)

async def queue(ctx):
    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.show_queue(ctx)

async def play(ctx, *args):
    if len(args) == 0:
        raise MissingParameter("song_name")

    musicservice = guildmanager.get_state(ctx.guild.id).music_service
    await musicservice.play(ctx, song_names=args)


COMMAND_MAPPINGS = {
    0: play,
    1: queue,
    2: skip
}