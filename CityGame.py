import json
import time

class CityGame:
    def __init__(self, synthesizer, recognizer):
        self.synthesizer = synthesizer
        self.recognizer = recognizer
        self.cities = set()
        self.last_letter = None
        self.available_cities = self.load_city_list()

    def load_city_list(self):
        try:
            with open("cities.txt", "r", encoding="utf-8") as file:
                cities = [line.strip().lower() for line in file.readlines()]
            return cities
        except FileNotFoundError:
            self.synthesizer.speak("Файл с городами не найден.")
            return []
        except Exception as e:
            self.synthesizer.speak(f"Ошибка при загрузке файла с городами: {e}")
            return []

    def start_game(self):
        self.synthesizer.speak("Давайте, Назовите город.")
        self.cities.clear()
        self.last_letter = None
        self.play_turn()

    def play_turn(self):
        user_city = self.wait_for_city()
        if not user_city:
            self.synthesizer.speak("Вы не назвали город. Игра окончена.")
            return

        if not self.is_valid_city(user_city):
            self.synthesizer.speak(f"{user_city} — недопустимый город. Попробуйте другой.")
            self.play_turn()
            return

        self.cities.add(user_city.lower())
        self.last_letter = self.get_last_valid_letter(user_city)

        bot_city = self.get_bot_city()
        if bot_city:
            self.synthesizer.speak(f"Мой город: {bot_city}.")
            self.last_letter = self.get_last_valid_letter(bot_city)
            self.cities.add(bot_city.lower())
            self.play_turn()
        else:
            self.synthesizer.speak("Я не могу придумать город. Вы победили!")

    def wait_for_city(self):
        user_city = self.wait_for_command()
        return user_city

    def is_valid_city(self, city):
        if city.lower() in self.cities:
            self.synthesizer.speak(f"{city} уже использован. Попробуйте другой.")
            return False
        if city.lower() not in self.available_cities:
            return False
        if self.last_letter and not city.lower().startswith(self.last_letter):
            return False
        return True

    def get_last_valid_letter(self, city):
        for letter in reversed(city.lower()):
            if letter not in 'ьый':
                return letter
        return None

    def get_bot_city(self):
        for city in self.available_cities:
            if city.lower() not in self.cities and city.lower().startswith(self.last_letter):
                return city
        return None

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

