from collections import namedtuple
from music.musicservice import MusicService

GuildState = namedtuple("GuildState", "music_service")

class GuildNotRegistered(Exception):
    def __init__(self):
        super().__init__("Guild not registered")


_guild_states = {} 

def register(*, guild_id):
    _guild_states[guild_id] = GuildState(music_service=MusicService())


def get_state(guild_id):
    if guild_id not in _guild_states.keys():
       raise GuildNotRegistered()

    return _guild_states[guild_id]