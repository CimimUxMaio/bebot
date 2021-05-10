import re

def params(message):
    open_i = message.find("[")
    if len(message) == 0 or open_i == -1:
        return []

    close_i = message[open_i:].find("]") + open_i
    param = message[open_i+1:close_i]
    return [param] + params(message[close_i+1:])


def parse_message(message):
    parameters = params(message)
    command_message = re.sub('\[(.*)\]', '', message).strip()
    return command_message, parameters