from bs4 import BeautifulSoup
import requests
import re

class WikipediaSearcher:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer
        self.base_url = "https://ru.wikipedia.org/wiki/"
        self.key_phrases = (
            'найди в википедии', 'что такое', 'в википедии',
            'поиск в википедии', 'вики', 'узнай что такое',
            'информация о','что значит', 'объясни что такое'
        )
        self.assistant_name = 'эмбер'  # Имя ассистента

    def clean_text(self, text):
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        text = text.strip()
        return text

    def match_key_phrase(self, user_input):
        for phrase in self.key_phrases:
            if phrase in user_input.lower():
                return True
        return False

    def extract_query(self, user_input):

        user_input = user_input.lower().replace(self.assistant_name, '').strip()


        for phrase in self.key_phrases:
            if phrase in user_input:
                user_input = user_input.replace(phrase, '').strip()

        return user_input.strip()

    def search(self, user_input):
        if not self.match_key_phrase(user_input):
            print("Запрос не соответствует ключевым фразам для поиска в Википедии.")
            return

        query = self.extract_query(user_input)
        if not query:
            self.synthesizer.speak("Не удалось распознать запрос для поиска.")
            return

        query = query.replace(" ", "_")
        self.synthesizer.speak(f"Ищу информацию в Википедии о {query.replace('_', ' ')}.")
        try:
            response = requests.get(self.base_url + query)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.select('p')

                for paragraph in paragraphs:
                    cleaned_text = self.clean_text(paragraph.get_text())
                    if cleaned_text and len(cleaned_text.split()) > 10:
                        self.synthesizer.speak(cleaned_text[:500])
                        return

                self.synthesizer.speak("Не удалось найти содержательное описание на странице.")
            else:
                self.synthesizer.speak("Не удалось получить данные с Википедии. Проверьте запрос.")
        except requests.RequestException:
            self.synthesizer.speak("Произошла ошибка при подключении к Википедии.")
