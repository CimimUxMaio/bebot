class ModelException(Exception):
    def __init__(self, message):
        super().__init__(message)

       
def MissingParameters(self, *param_names):
    return ModelException(f"Missing required argument{'s' if len(param_names) > 1 else ''}: {', '.join(param_names)}")


def LastUninterpretedCommandMessageMissing():
    return ModelException("Last uninterpreted command message is missing or has already been classified")


def InvalidSongName(song_name):
    return ModelException(f"Could not download the song: {song_name}. Incorrect format try another. This could be due to it being in playlist or livestream format")


def UserNotConnectedToVoiceChannel():
    return ModelException(f"You must be connected to a voice channel")


def CommandInterpretationException(command_message):
    return ModelException(f"Couldn't resolve \"{command_message}\" to a valid command")


def IndexOutOfBoundaries(index):
    return ModelException(f"There is no song at index {index}")