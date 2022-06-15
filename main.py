import speech_recognition as sr
import config
import model
import utils
import keyboard
import gui
from intents.alarm import Alarm
from intents.applications import Applications
# from intents.translation import Translation
from subprocess import Popen
from intents.youtube_search import YoutubeSearch
from model.model_training import TrainingModel
from intents.google_search import GoogleSearch


def the_command(recognizer):
    voice_input = ''
    try:
        with sr.Microphone() as source:
            print('Listening...')
            recognizer.adjust_for_ambient_noise(source=source, duration=0.2)
            audio = recognizer.listen(source=source, timeout=5, phrase_time_limit=5)
        voice_input = recognizer.recognize_google(audio)
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


def keyboard_activation():

    k = keyboard.is_pressed('ScrLk')

    if k is True:
        key = True
    else:
        key = False

    return key


if __name__ == '__main__':
    words = model.words
    classes = model.classes

    training_model = TrainingModel(words, classes, model.data_x, model.data_y)
    trained_model = training_model.train()

    recognizer = sr.Recognizer()
    os = config.OS_NAME

    session = False

    while True:
        session = keyboard_activation()
        command = the_command(recognizer)
        if command or command != '':
            intent = training_model.get_intent(trained_model, command)
            response = TrainingModel.get_response(intent, config.DATA)
            print(intent, ' : ', response)
            if intent == 'greeting':
                utils.speak(response=response)
                session = True
                # Popen('python gui/user_interface.py')
            elif session and intent == 'applications':
                Applications(response).launch(command)
                session = False
            elif session and intent == 'youtube_search':
                YoutubeSearch(command, response).launch()
                session = False
            elif session and intent == 'alarm':
                Alarm(command, response).start()
                session = False
            # elif session and intent == 'translate':
            #     Translation(command).translate()
            #     session = False
            elif session and intent == 'google_search':
                GoogleSearch(command, response).open()
                session = False
            elif session and intent == 'nothing':
                session = False
