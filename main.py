import os

import pyttsx3
import speech_recognition as sr

import config
import model
import utils
from intents.alarm import Alarm
from intents.application import Applications
from intents.youtube_search import YoutubeSearch
from model.model_training import TrainingModel


def read_voice_cmd(speech):
    voice_input = ''
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print('Listening...')
            audio = speech.listen(source=source, timeout=5, phrase_time_limit=5)
        voice_input = speech.recognize_google(audio)
        print('Input : {}'.format(voice_input))
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        print('Network error.')
    except sr.WaitTimeoutError:
        pass
    except TimeoutError:
        pass

    return voice_input.lower()


def play_sound(response, os_name):
    # Pentru MAC
    if os_name == 'Darwin':
        os.system(f'say "{response}"')
    else:
        engine.say(response)
        engine.runAndWait()


if __name__ == '__main__':
    words = model.words
    classes = model.classes

    training_model = TrainingModel(words, classes, model.data_x, model.data_y)
    trained_model = training_model.train()

    speech = sr.Recognizer()
    engine = pyttsx3.init()
    os = config.DEFAULT_OS_NAME

    session = False

    while True:
        command = read_voice_cmd(speech)
        if command or command != '':
            intent = training_model.get_intent(trained_model, command)
            response = TrainingModel.get_response(intent, config.DATA)
            print(intent, ' : ', response)

            if intent == 'greeting':
                utils.speak(response=response)
                session = True
                continue
            elif session and intent == 'applications':
                Applications(response).launch(command)
                session = False
                continue
            elif session and intent == 'youtube_search':
                YoutubeSearch(command, response).launch()
                session = False
                continue
            elif intent == 'alarm':
                Alarm(command, response).start()
                continue
