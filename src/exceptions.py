class ModelException(Exception):
    def __init__(self, message):
        super().__init__(message)

       
def InvalidSongName(song_name):
    return ModelException(f"Could not download the song: {song_name}. Incorrect format try another. This could be due to it being in playlist or livestream format")


def UserNotConnectedToVoiceChannel():
    return ModelException(f"You must be connected to a voice channel")


def IndexOutOfBoundaries(index):
    return ModelException(f"There is no song at index {index}")