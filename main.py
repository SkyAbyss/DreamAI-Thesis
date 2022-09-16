import subprocess
import sys
import speech_recognition as sr
import config
import model
import utils
import keyboard
from intents.alarm import Alarm
from intents.applications import Applications
# from intents.translation import Translation
from intents.youtube_search import YoutubeSearch
from model.model_training import TrainingModel
from intents.google_search import GoogleSearch


def the_command(recognizer):
    voice_input = ''
    try:
        with sr.Microphone() as source:
            print('Listening...')
            recognizer.adjust_for_ambient_noise(source=source, duration=0.2)
            recognizer.pause_threshold = 0.5
            audio = recognizer.listen(source=source, phrase_time_limit=5)
        voice_input = recognizer.recognize_google(audio)
        print('Input : {}'.format(voice_input))
    except (sr.UnknownValueError, sr.WaitTimeoutError, TimeoutError):
        pass
    except sr.RequestError:
        print('Network error.')

    return voice_input.lower()


def keyboard_activation():
    k = keyboard.is_pressed('ScrLk')
    return k


if __name__ == '__main__':
    words = model.words
    classes = model.classes
    interface = ''
    training_model = TrainingModel(words, classes, model.data_x, model.data_y)
    trained_model = training_model.train()
    recognizer = sr.Recognizer()
    os = config.OS_NAME
    session = False

    while True:
        command = the_command(recognizer)
        key_is_pressed = keyboard_activation()
        if command or command != '':
            intent = training_model.get_intent(trained_model, command)
            response = TrainingModel.get_response(intent, config.DATA)
            print(intent, ' : ', response)
            if intent == 'greeting':
                interface = subprocess.Popen([sys.executable, 'gui/user_interface.py', '--username', 'root'])
                utils.speak(response=response)
                session = True
            if session | key_is_pressed is True:
                if intent == 'applications':
                    Applications(response).launch(command)
                    interface.kill()
                    session = False
                elif intent == 'youtube_search':
                    YoutubeSearch(command, response).launch()
                    interface.kill()
                    session = False
                elif intent == 'alarm':
                    Alarm(command, response).start()
                    interface.kill()
                    session = False
                # elif session and intent == 'translate':
                #     Translation(command).translate()
                #     interface.kill()
                #     session = False
                elif intent == 'google_search':
                    GoogleSearch(command, response).open()
                    interface.kill()
                    session = False
                elif intent == 'nothing':
                    interface.kill()
                    session = False

            if intent == 'shut_down':
                utils.speak(response)
                interface.kill()
                exit()
