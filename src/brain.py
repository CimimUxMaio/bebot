import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import commands
import pickle
from unidecode import unidecode
import re


class __Brain:
    def __init__(self):
        self.__model = load_model("../NeuralNetwork/model.h5")
        with open("../NeuralNetwork/word_index.pkl", "rb") as word_index_file:
            self.__word_index = pickle.load(word_index_file)


    def identify_command(self, message):
        encoded_message = self.__encode_message(message)

        prediction = tf.reshape(self.__model.predict(encoded_message), [-1])

        best_index = np.argmax(prediction)
        
        if prediction[best_index] < 0.6:
            print([ round(p, 2) for p in prediction.numpy() ])
            return commands.unknown

        return commands.COMMAND_MAPPINGS[best_index]

    def __normalize_message(self, message):
        return unidecode(re.sub(r'[^\w\s]', '', message.lower()))

    def __tokenize_message(self, message):
        return np.array([ self.__word_index[word] for word in message.split() if word in self.__word_index ])

    def __padd_tokenized_message(self, tokenized_message):
        return tf.convert_to_tensor(pad_sequences(np.array([tokenized_message]), value=self.__word_index["<PAD>"], maxlen=10, padding="post"))

    def __encode_message(self, message):
        return self.__padd_tokenized_message(self.__tokenize_message(self.__normalize_message(message)))


BRAIN = __Brain()
