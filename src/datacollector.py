import enum
import csv


class LastCommandMessageMissingException(BaseException):
    def __init__(self):
        super().__init__("Last command message is missing or has already been classified")


class InvalidClassification(BaseException):
    def __init__(self, invalid_classification):
        super().__init__(f"{invalid_classification} is not a valid command classification")


def is_valid_classification(client, classification):
    return classification in [cmd.name for cmd in client.commands]

def check_classification(client, classification):
    if not is_valid_classification(client, classification):
        raise InvalidClassification(classification)


__last_command_message = None
def set_last_command_message(message):
    global __last_command_message
    __last_command_message = message

def classify_last_command_message(classification):
    global __last_command_message
    
    if __last_command_message is None:
        raise LastCommandMessageMissingException()

    last_message = __last_command_message
    __last_command_message = None

    with open("../NeuralNetwork/collected_data.csv", "a") as collected_data_file:
        csv_writer = csv.DictWriter(collected_data_file, ["sentence", "command"])
        new_row = { "sentence": last_message, "command": classification }
        csv_writer.writerow(new_row)

    return last_message