import torch
import sounddevice as sd
import threading
import logging


class SpeechSynthesizer:
    def __init__(self, language='ru', model_id='v4_ru', sample_rate=48000, speaker='kseniya', use_gpu=False):
        self.sample_rate = sample_rate
        self.speaker = speaker
        self.device = torch.device('cuda' if use_gpu and torch.cuda.is_available() else 'cpu')
        torch.set_num_threads(4)
        self.model = None
        self.callbacks = []
        self._lock = threading.Lock()  # Блокировка для предотвращения параллельного выполнения

        try:
            self.model, _ = torch.hub.load(
                repo_or_dir='snakers4/silero-models',
                model='silero_tts',
                language=language,
                speaker=model_id
            )
            self.model.to(self.device)
            logging.info(f"Модель успешно загружена на {self.device}")
        except Exception as e:
            logging.error(f"Ошибка при загрузке модели: {e}")
            raise RuntimeError("Не удалось загрузить модель синтеза речи")

    def register_callback(self, callback):
        if callable(callback):
            self.callbacks.append(callback)
        else:
            logging.warning("Попытка зарегистрировать некорректный коллбэк")

    def _notify(self, event):
        for callback in self.callbacks:
            try:
                logging.info(f"Выполнение коллбэка для события: {event}")
                callback(event)
            except Exception as e:
                logging.error(f"Ошибка в коллбэке: {e}")

    def speak(self, text):
        if not text or not isinstance(text, str):
            logging.warning("Пустой или некорректный текст для синтеза")
            return

        if sd.query_devices(kind='output')['max_output_channels'] < 1:
            logging.warning("Аудиоустройство не поддерживает воспроизведение")
            return

        if not self._lock.acquire(blocking=False):  # Проверяем, занята ли блокировка
            logging.warning("Синтез речи уже выполняется")
            return

        try:
            self._notify("start")
            logging.info("Начат синтез речи")
            audio = self.model.apply_tts(
                text=text,
                speaker=self.speaker,
                sample_rate=self.sample_rate
            )
            logging.info("Синтез завершен, начинается воспроизведение")
            sd.play(audio.cpu().numpy(), self.sample_rate)
            sd.wait()  # Ждём завершения воспроизведения
            logging.info("Воспроизведение завершено")
            self._notify("end")
        except Exception as e:
            logging.error(f"Ошибка при синтезе речи или воспроизведении: {e}")
            self._notify("error")
        finally:
            self._lock.release()  # Освобождаем блокировку

    def stop(self):
        try:
            sd.stop()
            logging.info("Воспроизведение остановлено")
            self._notify("stop")
        except Exception as e:
            logging.error(f"Ошибка при остановке воспроизведения: {e}")


# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
