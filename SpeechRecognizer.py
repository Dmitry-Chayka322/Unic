from vosk import Model, KaldiRecognizer
import logging
import queue
import sounddevice as sd
import json
import threading

class SpeechRecognizer:
    def __init__(self, model_path='model'):
        self.q = queue.Queue()
        self.running = threading.Event()
        self.running.set()

        try:
            self.model = Model(model_path)
            self.recognizer = KaldiRecognizer(self.model, 16000)
            logging.info("Модель успешно загружена")
        except Exception as e:
            logging.error(f"Ошибка при инициализации модели: {e}")
            raise e

    def start_listening(self, callback):
        def audio_callback(indata, frames, time, status):
            if status:
                logging.warning(f"Ошибка аудиопотока: {status}")
            self.q.put(bytes(indata))

        def processing_thread():
            logging.info("Голосовой помощник запущен. Скажите что-нибудь...")

            while self.running.is_set():
                try:
                    data = self.q.get(timeout=1)
                    if self.recognizer.AcceptWaveform(data):
                        result = json.loads(self.recognizer.Result())
                        if result.get('text'):
                            command = result['text']
                            logging.info(f"Вы сказали: {command}")
                            callback(command)
                    else:
                        partial_result = json.loads(self.recognizer.PartialResult())
                        if partial_result.get('text'):
                            logging.info(f"Частичный результат: {partial_result['text']}")
                            callback(partial_result['text'], partial=True)
                except queue.Empty:
                    logging.debug("Очередь пуста. Ожидание данных...")
                except Exception as e:
                    logging.error(f"Ошибка обработки данных: {e}")

        threading.Thread(target=processing_thread, daemon=True).start()

        try:
            with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',
                                   channels=1, callback=audio_callback):
                while self.running.is_set():
                    sd.sleep(100)
        except Exception as e:
            logging.error(f"Ошибка аудиопотока: {e}")

    def stop_listening(self):
        try:
            self.running.clear()
            logging.info("Прослушивание остановлено")
        finally:
            logging.info("Ресурсы освобождены")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("speech_recognizer.log"), logging.StreamHandler()]
)
