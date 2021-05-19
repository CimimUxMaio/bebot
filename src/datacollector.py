import csv
from exceptions import LastUninterpretedCommandMessageMissing


__last_message = None
def set_last_message(message):
    global __last_message
    __last_message = message

def classify_last_message(classification):
    global __last_message
    
    if __last_message is None:
        raise LastUninterpretedCommandMessageMissing()

    last_message = __last_message
    __last_message = None

    with open("../NeuralNetwork/collected_data.csv", "a") as collected_data_file:
        csv_writer = csv.DictWriter(collected_data_file, ["sentence", "command"])
        new_row = { "sentence": last_message, "command": classification }
        csv_writer.writerow(new_row)

    return last_message