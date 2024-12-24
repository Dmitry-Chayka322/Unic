import subprocess

class Open_app:
    def __init__(self, synthesizer):
        self.synthesizer = synthesizer
        self.app_path = {
             "browser": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "telegram": "D:\\Telegram Desktop\\Telegram.exe",
            "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
            "steam": "D:\\Steam\\steam.exe",
            "discord": "C:\\Users\\User\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe",
            "blander": "D:\\blender\\blender-launcher.exe"

        }

        self.app_name = {

             "browser": (
                "открой браузер", "запусти браузер", "открой яндекс", "открой хром",
                "открой интернет",),
            "telegram": (
                "открой телегу", "запусти телеграмм", "открой телеграмм",
                "открой сообщения", "хочу написать в телеге", "телеграм",
                "включи телегу", "запусти чат", "открой мессенджер"
            ),
            "word": (
                "открой ворд", "запусти ворд", "открой текстовый редактор",
                "включи ворд", "начни редактировать текст", "документ",
                "запусти текстовый документ", "открой текст"
            ),
            "excel": (
                "открой эксель", "запусти эксель",
                "включи эксель", "начни работу с таблицей", "таблицы",
                "открой таблицы", "запусти электронную таблицу",
            ),
            "steam": (
                "открой стим", "запусти стим", "хочу играть",
                "запусти мои игры", "включи игры", "запусти платформу игр",
                 "поиграем"
            ),
            "discord": (
                "открой дискорд", "запусти дискорд",
                "включи дискорд", "открой чат с друзьями",
                "запусти связь", "открой голосовой чат"
            ),
            "blender": (
                "запусти блендер", "открой блендер", "хочу моделировать",
                "открой программу для моделирования"
            ),
            "pycharm": (
                "запусти питон", "открой питон",
                 "открой среду разработки", "программирование",
                "начни писать код", "запусти python", "работа с кодом"
            )
        }

    def open_app(self, command):
        for app, keywords in self.app_name.items():
            if any(keyword in command for keyword in keywords):
                app_path = self.app_path.get(app)
                if app_path:
                    try:
                        subprocess.Popen(app_path, shell=True)

                    except Exception as e:
                        self.synthesizer.speak(f"Не удалось открыть приложение. Ошибка: {str(e)}")
                else:
                    self.synthesizer.speak(f"Путь к приложению не найден.")
                return
        self.synthesizer.speak("Приложение не распознано.")