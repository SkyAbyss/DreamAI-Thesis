import config
import html
import utils

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from model.voice_analyzer import VoiceAnalyzer

import re


class YoutubeSearch:
    DEVELOPER_KEY = "AIzaSyDBkNCCDungBJWGjF9wc-7CvTOEvgjwsWQ"
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_VERSION = 'v3'

    def __init__(self, command, response):
        self.command = command
        self.response = response
        self.os = config.DEFAULT_OS_NAME

    def get_search_value(self):
        intents = config.DATA['intents']
        utterances = [intent['utterances'] for intent in intents if intent['tag'] == 'youtube_search'][0]
        words = set([word for utterance in utterances for word in utterance.split(' ')])
        words = '|'.join(words)
        return re.sub(words, '', self.command).strip()

    def search(self):
        try:
            youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_VERSION, developerKey=self.DEVELOPER_KEY)
            search = self.get_search_value()
            search_response = youtube.search().list(
                q=search,
                part='id, snippet',
                maxResults=1
            ).execute()

            return search_response.get('items')

        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occurred: {e.content}')

    def open(self, url):
        sentiments = VoiceAnalyzer().recognize()
        if sentiments:
            max_key = max(sentiments, key=sentiments.get)
            if max_key == 'neu' or max_key == 'pos':
                utils.open(url)
                utils.speak(self.response)

    def launch(self):
        try:
            result = self.search()[0]
        except Exception as e:
            print(e)
        title = html.unescape(result['snippet']['title'])
        if result['id']['kind'] == 'youtube#video':
            utils.speak(f'I have found the video as {title}. Would you like to play it?')
            url = f"https://youtu.be/{result['id']['videoId']}"
        elif result['id']['kind'] == 'youtube#channel':
            utils.speak(f'I got a channel for you as {title}. Would you like to open it?')
            url = f"https://www.youtube.com/channel/{result['id']['channelId']}"

        self.open(url)
