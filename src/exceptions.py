class ModelException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UnknownCommandException(ModelException):
    def __init__(self, command_message):
        self.command_message = command_message
        super().__init__(f"Couldn't resolve \"{command_message}\" to a valid command")


class LastUninterpretedCommandMessageMissingException(ModelException):
    def __init__(self):
        super().__init__("Last uninterpreted command message is missing or has already been classified")


class InvalidClassification(ModelException):
    def __init__(self, invalid_classification):
        super().__init__(f"\"{invalid_classification}\" is not a valid command classification")