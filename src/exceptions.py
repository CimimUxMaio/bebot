class ModelException(Exception):
    def __init__(self, message):
        super().__init__(message)


class MissingParameter(ModelException):
    def __init__(self, param_name):
        super().__init__(f"{param_name} is a required argument that is missing")
        

class LastUninterpretedCommandMessageMissing(ModelException):
    def __init__(self):
        super().__init__("Last uninterpreted command message is missing or has already been classified")


class InvalidSongName(ModelException):
    def __init__(self, song_name):
        super().__init__(f"Could not download the song: {song_name}. Incorrect format try another. This could be due to it being in playlist or livestream format")


class UserNotConnectedToVoiceChannel(ModelException):
    def __init__(self):
        super().__init__(f"You must be connected to a voice channel")


async def handle_model_error(ctx, error):
    if isinstance(error, ModelException):
        await ctx.send(str(error))
    