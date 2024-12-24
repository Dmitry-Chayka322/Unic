import json
import os
from datetime import datetime

class NoteManager:
    def __init__(self, file_name="notes.json"):
        self.file_name = file_name
        self.notes = self._load_notes()

    def _load_notes(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Ошибка загрузки заметок. Файл поврежден.")
                return []
        return []


    def _save_notes(self):
        try:
            with open(self.file_name, "w", encoding="utf-8") as file:
                json.dump(self.notes, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения заметок: {e}")

    def create_note(self, text):
        note = {
            "text": text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"Добавляем заметку: {note}")
        self.notes.append(note)
        self._save_notes()
        self.notes = self._load_notes()

    def get_notes(self):
        self.notes = self._load_notes()
        print(f"Загружаем заметки: {self.notes}")
        return self.notes

    def delete_all_notes(self):
        self.notes = []
        self._save_notes()

    def delete_notes_by_indices(self, indices):
        valid_indices = [i for i in indices if 0 <= i < len(self.notes)]
        if len(valid_indices) != len(indices):
            print("Некорректные индексы, некоторые заметки не были удалены.")
            return False
        for idx in sorted(valid_indices, reverse=True):
            self.notes.pop(idx)
        self._save_notes()
        return True
