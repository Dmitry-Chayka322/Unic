import requests
from num2words import num2words
class CurrencyRateFetcher:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer
        self.api_url = "https://www.cbr-xml-daily.ru/daily_json.js"

    def get_currency_rate(self, currency_code):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            if currency_code in data["Valute"]:
                valute_data = data["Valute"][currency_code]
                rate = valute_data["Value"]
                rate_text = num2words(int(rate), lang='ru')
                name = valute_data["Name"]
                self.synthesizer.speak(f"Курс {name} составляет {rate_text} рублей.")
            else:
                self.synthesizer.speak(f"Извините, я не нашла информацию о валюте {currency_code}.")
        except Exception as e:
            self.synthesizer.speak("Не удалось получить информацию о курсе валют. Проверьте подключение к интернету.")
            print(f"Ошибка при запросе курса валют: {e}")
