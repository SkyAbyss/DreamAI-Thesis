import webbrowser
import utils
from model.voice_analyzer import VoiceAnalyzer


class GoogleSearch:
    INTENT_NAME = 'google_search'

    def __init__(self, command, response):
        self.command = command
        self.response = response

    def search(self):
        search = utils.get_search_value(self.command, GoogleSearch.INTENT_NAME)

    def open(self, search):
        sentiments = VoiceAnalyzer().get_polarity_scores()
        if sentiments:
            max_key = max(sentiments, key=sentiments.get)
            if max_key == 'neu' or max_key == 'pos':
                utils.speak(self.response)
                webbrowser.open_new(f'https://www.google.com/search?q={search}')


