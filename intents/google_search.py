import webbrowser
import utils
from model.voice_analyzer import VoiceAnalyzer


class GoogleSearch:
    INTENT_NAME = 'google_search'

    def __init__(self, command, response):
        self.command = command
        self.response = response

    def open(self):
        search = utils.get_search_value(self.command, GoogleSearch.INTENT_NAME)
        utils.speak(self.response)
        utils.speak(search)
        utils.speak('Do you want to search it?')
        sentiments = VoiceAnalyzer().get_polarity_scores()
        if sentiments:
            max_key = max(sentiments, key=sentiments.get)
            if max_key == 'neu' or max_key == 'pos':
                webbrowser.open_new(f'https://www.google.com/search?q={search}')
