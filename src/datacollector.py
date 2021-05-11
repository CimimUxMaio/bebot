import csv
from exceptions import InvalidClassification, LastUninterpretedCommandMessageMissing


def is_valid_classification(client, classification):
    return classification in [cmd.name for cmd in client.commands]

def check_classification(client, classification):
    if not is_valid_classification(client, classification):
        raise InvalidClassification(classification)


__last_uninterpreted_message = None
def set_last_uninterpreted_message(message):
    global __last_uninterpreted_message
    __last_uninterpreted_message = message

def classify_last_uninterpreted_message(classification):
    global __last_uninterpreted_message
    
    if __last_uninterpreted_message is None:
        raise LastUninterpretedCommandMessageMissing()

    last_message = __last_uninterpreted_message
    __last_uninterpreted_message = None

    with open("../NeuralNetwork/collected_data.csv", "a") as collected_data_file:
        csv_writer = csv.DictWriter(collected_data_file, ["sentence", "command"])
        new_row = { "sentence": last_message, "command": classification }
        csv_writer.writerow(new_row)

    return last_message