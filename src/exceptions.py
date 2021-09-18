from discord.ext import commands


class ModelException(commands.CommandError):
    def __init__(self, message):
        super().__init__(message)

       
def InvalidSongName(song_name):
    return ModelException(f"Could not download the song: {song_name}. Incorrect format try another. This could be due to it being in playlist or livestream format")


def UserNotConnectedToVoiceChannel():
    return ModelException(f"You must be connected to a voice channel")


def BotIsConnectedToAnotherChanel():
    return ModelException("Bot is already in a voice channel")


def NothingIsCurrentlyPlaying():
    return ModelException("There is not any music playing right now")


def IndexOutOfBoundaries(index):
    return ModelException(f"There is no song at index {index}")