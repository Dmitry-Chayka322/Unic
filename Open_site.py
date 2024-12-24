import webbrowser

class Open_site:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer
        self.site_name  = {
            "youtube": ('открой ютуб', 'включи видоски'),
            "vk": ('открой вконтакте', 'хочу полистать ленту'),
            "kinopoisk": ('открой кинопоиск',),
            "map": ('открой карты', 'хочу узнать маршрут'),
            "github": ('открой гит', ),
            "mail": ('открой почту', 'хочу проверить письма'),
            "music": ('открой музыку', 'хочу что нибудь послушать'),
            "cdo": ('открой цдо', 'хочу узнать задание'),
            "practicum": ('открой практикум',)

        }
        self.site_path = {
            "youtube": 'https://www.youtube.com/',
            "vk": 'https://vk.com/',
            "kinopoisk": 'https://hd.kinopoisk.ru/',
            "map": 'https://yandex.ru/maps/',
            "github": 'https://github.com/',
            "mail": 'https://mail.yandex.ru/',
            "music": 'https://next.music.yandex.ru/',
            "cdo": 'https://cs.cdo.vlsu.ru/',
            "practicum": 'https://practicum.yandex.ru/',

        }

    def open_site(self, command):
        for site, keywords in self.site_name.items():
            if any(keyword in command for keyword in keywords):
                url = self.site_path.get(site)
                if url:
                    webbrowser.open(url)
                else:
                    self.synthesizer.speak(f"Не удалось найти ссылку для сайта {site}")
                break
        else:
            self.synthesizer.speak("Не удалось найти сайт в списке доступных.")