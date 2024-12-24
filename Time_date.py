from datetime import datetime
from num2words import num2words

class Time_Date:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer

    def time_command(self):
        now = datetime.now()
        current_time = "Сейч+ас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
        self.synthesizer.speak(current_time)

    def date_command(self):
        now = datetime.now()
        current_date = "Сегодня " + num2words(now.day, lang='ru') + " " + num2words(now.month, lang='ru')
        self.synthesizer.speak(current_date)