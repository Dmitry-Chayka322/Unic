import os
import sys
import json
import threading
import time
from datetime import datetime
import SpeechSynthesizer
import SpeechRecognizer
import NoteManager
import WeatherFetcher
import Time_date
import Open_app
import Open_site
import Wiki
import webbrowser
import tkinter as tk
from PIL import Image, ImageTk
import CityGame
from CurrencyRateFetcher import CurrencyRateFetcher

class CommandExecutor:
    def __init__(self, synthesizer, recognizer):
        self.synthesizer = synthesizer
        self.recognizer = recognizer
        self.note_manager = NoteManager.NoteManager()
        self.weather_fetcher = WeatherFetcher.WeatherFetcher(synthesizer)
        self.time_date = Time_date.Time_Date(synthesizer)
        self.currency_rate_fetcher = CurrencyRateFetcher(synthesizer)
        self.city_game = CityGame.CityGame(synthesizer, recognizer)
        self.open_app = Open_app.Open_app(synthesizer)
        self.open_site = Open_site.Open_site(synthesizer)
        self.wiki = Wiki.WikipediaSearcher(synthesizer)
        self.command = {

            "ctime": (
                'время', 'текущее время', 'сейчас времени', 'который час',
                'какое время', 'скажи время', 'часов сколько', 'который час сейчас',
                'сколько времени', 'время сейчас'
            ),
            "shutdown": (
                'выключи компьютер', 'отдохни', 'завершение работы',
                'выключайся', 'отключись', 'остановись', 'засни',
                'выключить систему', 'заверши работу', 'спи', 'выключись'
            ),
            "weather": (
                'погода', 'как на улице', 'прогноз погоды',
                'какая погода', 'что за погода', 'скажи погоду',
                'погода сейчас', 'на улице как', 'на улице погода',
                'сейчас погода', 'погода на сегодня'
            ),
            "wiki": (
                'найди в википедии', 'что такое', 'в википедии',
            'поиск в википедии', 'вики', 'узнай что такое',
            'информация о', 'расскажи про', 'что значит', 'объясни что такое'
            ),
            "date": (
                'какое число', 'какой сегодня день', 'какое сегодня число',
                'дата сегодня', 'какая дата', 'сегодняшняя дата',
                'скажи число', 'день недели', 'сегодня какой день',
                'сегодня какое число'
            ),
            "create_note": (
                'сделай заметку', 'запиши', 'запомни', 'добавь заметку',
                'новая заметка', 'создай заметку', 'запиши это',
                'создать заметку', 'запиши в заметки', 'запомни это'
            ),
            "currency_rate": (
                'курс валют', 'какой курс', 'узнай курс', 'валюта',
                'курс доллара', 'курс евро', 'обмен валют',
                'валютный курс', 'узнай курс валют', 'сколько стоит доллар',
                'какой курс доллара', 'обменный курс'
            ),
            "play_movie": (
                'включи фильм', 'посмотри фильм', 'найди фильм',
                'открой фильм', 'поищи фильм', 'запусти фильм',
                'посмотреть фильм', 'поиск фильма', 'включить кино',
                'кино', 'фильм хочу посмотреть', 'фильм включи'
            ),
            "city_game": (
                'сыграем в города', 'игра в города', 'давай в города',
                'города', 'поиграем в города', 'играть в города',
                'начнем города', 'давай играть в города', 'города начнем',
                'играем в города', 'сыграем в игру города'
            ),
        }


        self.assistant_name = "эмбер"
        self.awaiting_command = False

    def execute(self, command):
        command = command.lower()

        if not self.awaiting_command:
            if command.startswith(self.assistant_name):
                self.awaiting_command = True
            else:
                return
        else:
            self.awaiting_command = False
            command = command[len(self.assistant_name):].strip()

        if any(keyword in command for keyword in self.command['ctime']):
            self.time_date.time_command()
        elif any(keyword in command for keyword in self.command['date']):
            self.time_date.date_command()
        elif any(keyword in command for keyword in self.command['weather']):
            self.weather_fetcher.get_weather()
        elif any(keyword in command for keyword in self.command['create_note']):
            self.create_note_interactive()
        elif any(keyword in command for keyword in self.command['shutdown']):
            self.shutdown_computer()
        elif any(keyword in command for keyword in self.command['currency_rate']):
            self.fetch_currency_rate(command)
        elif any(keyword in command for keyword in [kw for kws in self.open_site.site_name.values() for kw in kws]):
            self.open_site.open_site(command)
        elif any(keyword in command for keyword in self.command['wiki']):
            self.search_wikipedia(command)
        elif any(keyword in command for keyword in [kw for kws in self.open_app.app_name.values() for kw in kws]):
            self.open_app.open_app(command)
        elif any(keyword in command for keyword in self.command['play_movie']):
            self.play_movie(command)
        elif any(keyword in command for keyword in self.command['city_game']):
            self.city_game.start_game()

    def play_movie(self, command):
        self.synthesizer.speak("Какой фильм вы хотите посмотреть?")
        movie_name = self.wait_for_command(timeout=15)
        if movie_name:
            movie_name = movie_name.strip()
            print(f"Получено название фильма: {movie_name}")
            search_url = f"https://okko.tv/search/{movie_name}"
            webbrowser.open(search_url)
            self.synthesizer.speak(f"Ищу фильм {movie_name}.")
        else:
            self.synthesizer.speak("Извините, я не расслышала название фильма.")

    def search_wikipedia(self, command):
        query = command.replace(" эмбер найди в википедии", "").replace("эмбер что такое", "").strip()
        self.wiki.search(query)

    def create_note_interactive(self):
        self.synthesizer.speak("Что вы хотите записать....")
        note = self.wait_for_command()
        if note:
            self.note_manager.create_note(note)
            self.synthesizer.speak("Заметка сохранена....  ")
        else:
            self.synthesizer.speak("Извините, я не расслышала.")

    def shutdown_computer(self):
        self.synthesizer.speak("Вы уверены, что хотите выключить компьютер? Скажите 'да' для подтверждения.")
        confirmation = self.wait_for_command()
        if confirmation and 'да' in confirmation.lower():
            self.synthesizer.speak("Выключаю компьютер. До свидания!")
            if sys.platform == 'win32':
                os.system("shutdown /s /t 5")
            else:
                os.system("shutdown -h now")
        else:
            self.synthesizer.speak("Отмена выключения.")

    def fetch_currency_rate(self, command):
        self.synthesizer.speak("Какую валюту вы хотите узнать? ")
        user_input = self.wait_for_command().strip().lower()
        CURRENCY_CODES = {
            "доллар": "USD",
            "евро": "EUR",
            "юань": "CNY",
            "фунт": "GBP",
            "йена": "JPY",
            "дирхам": "AED",
            "белорусский рубль": "BYN",
        }

        currency_code = CURRENCY_CODES.get(user_input, user_input.upper())

        if currency_code:
            self.currency_rate_fetcher.get_currency_rate(currency_code)
        else:
            self.synthesizer.speak("Я не нашла такую валюту.")

    def wait_for_command(self, timeout=10):
        start_time = time.time()
        while True:
            data = self.recognizer.q.get()
            if self.recognizer.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.recognizer.Result())
                if result.get('text'):
                    return result['text']

            if time.time() - start_time > timeout:
                self.synthesizer.speak("Превышено время ожидания. Попробуйте снова.")
                return None

class VoiceAssistant:
    def __init__(self):
        self.synthesizer = SpeechSynthesizer.SpeechSynthesizer()
        self.recognizer = SpeechRecognizer.SpeechRecognizer()
        self.command_executor = CommandExecutor(self.synthesizer, self.recognizer)
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            greeting = self.get_greeting()
            self.synthesizer.speak(greeting)
            recognizer_thread = threading.Thread(target=self.recognizer.start_listening,
                                                 args=(self.command_executor.execute,))
            recognizer_thread.start()

    def stop(self):
        self.is_running = False
        self.recognizer.stop_listening()
        self.synthesizer.speak("Ассистент остановлен.")

    @staticmethod
    def get_greeting():
        current_hour = datetime.now().hour
        if 6 <= current_hour < 12:
            return "Доброе утро!"
        elif 12 <= current_hour < 18:
            return "Добрый день!"
        elif 18 <= current_hour < 23:
            return "Добрый вечер!"
        else:
            return "Здравствуйте!"


class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.is_running = False
        self.is_microphone_on = True
        self.is_dark_mode = False
        self.root = tk.Tk()

        self.root.title("Эмбер")
        self.root.geometry("500x350")
        self.root.config(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.logo_label = None
        self.toggle_microphone_btn = None
        self.canvas = None
        self.theme_button = None
        self.sun_image = None
        self.moon_image = None

        self.create_widgets()

    def create_widgets(self):

        logo_image = Image.open("лого.png").resize((220, 220), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_label = tk.Label(self.root, image=self.logo_photo, bg="#FFFFFF")
        self.logo_label.bind("<Button-1>", self.toggle_assistant)
        self.logo_label.pack(pady=40)


        self.canvas = tk.Canvas(self.root, width=20, height=20, bg="#FFFFFF", highlightthickness=0)
        self.circle = self.canvas.create_oval(0, 0, 20, 20, fill="#FF0000")
        self.canvas.place(relx=0.02, rely=0.95, anchor="sw")


        self.toggle_microphone_btn = tk.Button(self.root, text="Микрофон", font=("Arial", 10, "bold"),
                                               command=self.toggle_microphone, width=8, height=1, bg="#3F51B5",
                                               fg="white", relief="flat")
        self.toggle_microphone_btn.place(x=420, y=300)


        self.sun_image = ImageTk.PhotoImage(Image.open("sun.png").resize((24, 24), Image.Resampling.LANCZOS))
        self.moon_image = ImageTk.PhotoImage(Image.open("moon.png").resize((24, 24), Image.Resampling.LANCZOS))

        self.theme_button = tk.Button(self.root, image=self.moon_image, bg="#FFFFFF", command=self.toggle_theme,
                                      relief="flat", highlightthickness=0)
        self.theme_button.place(x=460, y=10)

    def toggle_assistant(self, event=None):
        if self.is_running:
            self.assistant.stop()
            self.is_running = False
            self.canvas.itemconfig(self.circle, fill="#FF0000")
        else:
            self.assistant.start()
            self.is_running = True
            self.canvas.itemconfig(self.circle, fill="#00FF00")

    def toggle_microphone(self):
        if self.is_microphone_on:
            self.assistant.recognizer.stop_listening()
            self.is_microphone_on = False
            self.toggle_microphone_btn.config(text="Вкл. микрофон", bg="#8BC34A")
        else:
            self.assistant.recognizer.start_listening(self.assistant.command_executor.execute)
            self.is_microphone_on = True
            self.toggle_microphone_btn.config(text="Выкл. микрофон", bg="#FF5722")

    def toggle_theme(self):
        if self.is_dark_mode:
            self.is_dark_mode = False
            self.root.config(bg="#FFFFFF")
            self.logo_label.config(bg="#FFFFFF")
            self.canvas.config(bg="#FFFFFF")
            self.theme_button.config(image=self.moon_image, bg="#FFFFFF")
            self.toggle_microphone_btn.config(bg="#3F51B5", fg="white")
        else:
            self.is_dark_mode = True
            self.root.config(bg="#121212")
            self.logo_label.config(bg="#121212")
            self.canvas.config(bg="#121212")
            self.theme_button.config(image=self.sun_image, bg="#121212")
            self.toggle_microphone_btn.config(bg="#1E88E5", fg="white")



if __name__ == "__main__":
    assistant = VoiceAssistant()
    gui = AssistantGUI(assistant)
    gui.root.mainloop()