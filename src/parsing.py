

def params(message):
    open_i = message.find("[")
    if len(message) == 0 or open_i == -1:
        return []

    close_i = message[open_i:].find("]") + open_i
    param = message[open_i+1:close_i]
    return [param] + params(message[close_i+1:])


def parse_message(message):
    parameters = params(message)

    words = message.split()
    command_message_words = []
    for word in words:
        if word not in parameters:
            command_message_words.append(word)

    return ' '.join(command_message_words), parameters