class ModelException(Exception):
    def __init__(self, message):
        super().__init__(message)


class MissingParameter(ModelException):
    def __init__(self, param_name):
        super().__init__(f"{param_name} is a required argument that is missing.")
        

class LastUninterpretedCommandMessageMissing(ModelException):
    def __init__(self):
        super().__init__("Last uninterpreted command message is missing or has already been classified")


class InvalidClassification(ModelException):
    def __init__(self, invalid_classification):
        super().__init__(f"\"{invalid_classification}\" is not a valid command classification")