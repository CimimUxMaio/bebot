from collections import namedtuple
import musicservice

GuildState = namedtuple("GuildState", "music_service")


_guild_states = {} 

class GuildNotRegistered(Exception):
    def __init__(self):
        super().__init__("Guild not registered")


def register(*, guild_id):
    _guild_states[guild_id] = GuildState(music_service=musicservice.MusicService())


def get_state(guild_id):
    if guild_id not in _guild_states.keys():
       raise GuildNotRegistered()

    return _guild_states[guild_id]