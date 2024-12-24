import requests
from num2words import num2words

class WeatherFetcher:
    def __init__(self,synthesizer, api_key = '433714c54059169fede91b0fb1f70572'):
        self.synthesizer = synthesizer
        self.api_key = api_key
        self.city = 'Владимир'

    def get_weather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': self.city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if response.status_code == 200:
                weather_description = data['weather'][0]['description'].capitalize()
                temp = round(data['main']['temp'])
                temp_text = num2words(int(temp), lang='ru')

                weather_report = (
                    f"Сейчас в городе {self.city} {weather_description}. "
                    f"Температура воздуха {temp_text} градусаов"
                )
                self.synthesizer.speak(weather_report)
            else:
                error_message = data.get('message', 'Ошибка при получении данных о погоде.')
                self.synthesizer.speak(f"Не удалось получить погоду для города {self.city}. Ошибка: {error_message}")

        except requests.exceptions.RequestException as e:
            self.synthesizer.speak(f"Произошла ошибка при обращении к сервису погоды: {e}")

