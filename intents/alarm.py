import threading
from datetime import datetime

import utils
from utils.alarm_utils.alarm_timing import AlarmTiming


class Alarm(threading.Thread):
    def __init__(self, voice_input, response):
        threading.Thread.__init__(self)
        self.input = voice_input
        self.response = response

    def run(self):
        new = AlarmTiming(self.input).get_expected_time()
        if new:
            new = datetime.strptime(new, "%Y-%m-%d %H:%M:00")
            print('Current time is : ' + str(datetime.now()))
            if datetime.now() > new:
                utils.speak('Current time is greater than the requested alarm time.')
            else:
                utils.speak(self.response)
                while True:
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:00')
                    now = datetime.strptime(now, "%Y-%m-%d %H:%M:00")
                    if now == new:
                        utils.speak('Bip boop bip boop! My circuits tell me that your time is up.')
                        break
