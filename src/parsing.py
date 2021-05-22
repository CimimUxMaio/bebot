import re
import config

OPENER = config.PARAM_WRAPPERS[0]
CLOSER = config.PARAM_WRAPPERS[1]

def params(message):
    open_i = message.find(OPENER)
    if len(message) == 0 or open_i == -1:
        return []

    relative_close_i = message[open_i+1:].find(CLOSER) + 1
    if relative_close_i == 0:
        return []

    close_i = relative_close_i + open_i
    param = message[open_i+1:close_i]
    return [param] + params(message[close_i+1:])


def parse_message(message):
    parameters = params(message)
    command_message = re.sub(f'\{OPENER}(.*)\{CLOSER}', '', message).strip()
    return command_message, parameters