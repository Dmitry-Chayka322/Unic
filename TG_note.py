import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from NoteManager import NoteManager

note_manager = NoteManager()

TOKEN = "7715793570:AAEc889N_ob50unTZVEp18476bKK6MzhDzw"
bot = telebot.TeleBot(TOKEN)


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("📝 Заметки"))
    return markup


def notes_menu(has_notes):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(KeyboardButton("✏️ Добавить заметку"))

    if has_notes:
        markup.add(KeyboardButton("📄 Показать все заметки"))
        markup.add(KeyboardButton("❌ Удалить все заметки"))
        markup.add(KeyboardButton("🗑️ Удалить заметки по индексам"))

    markup.add(KeyboardButton("⬅️ Назад"))
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в менеджер заметок! Выберите категорию:",
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda msg: msg.text == "📝 Заметки")
def open_notes_menu(message):
    has_notes = len(note_manager.get_notes()) > 0
    bot.send_message(
        message.chat.id,
        "Выберите действие с заметками:",
        reply_markup=notes_menu(has_notes)
    )


@bot.message_handler(func=lambda msg: msg.text == "✏️ Добавить заметку")
def add_note_prompt(message):
    msg = bot.send_message(
        message.chat.id,
        "Введите текст заметки:"
    )
    bot.register_next_step_handler(msg, add_note)


def add_note(message):
    note_manager.create_note(message.text)
    bot.send_message(
        message.chat.id,
        "✅ Заметка добавлена!",
        reply_markup=notes_menu(has_notes=True)
    )


@bot.message_handler(func=lambda msg: msg.text == "📄 Показать все заметки")
def show_notes(message):
    notes = note_manager.get_notes()
    if not notes:
        bot.send_message(message.chat.id, "❗ Заметок пока нет.")
    else:
        response = "\n\n".join(
            [f"#{idx} - {note['text']} (время: {note['timestamp']})"
             for idx, note in enumerate(notes)]
        )
        bot.send_message(message.chat.id, response)


@bot.message_handler(func=lambda msg: msg.text == "❌ Удалить все заметки")
def delete_all_notes(message):
    note_manager.delete_all_notes()
    bot.send_message(
        message.chat.id,
        "🗑️ Все заметки удалены.",
        reply_markup=notes_menu(has_notes=False)
    )


@bot.message_handler(func=lambda msg: msg.text == "🗑️ Удалить заметки по индексам")
def delete_notes_prompt(message):
    msg = bot.send_message(
        message.chat.id,
        "Введите индексы заметок для удаления через запятую (например: 0,2,4):"
    )
    bot.register_next_step_handler(msg, delete_notes_by_indices)


def delete_notes_by_indices(message):
    try:
        indices = list(map(int, message.text.split(",")))
        success = note_manager.delete_notes_by_indices(indices)
        has_notes = len(note_manager.get_notes()) > 0
        if success:
            bot.send_message(
                message.chat.id,
                "✅ Указанные заметки удалены.",
                reply_markup=notes_menu(has_notes)
            )
        else:
            bot.send_message(
                message.chat.id,
                "⚠️ Ошибка: один или несколько индексов не найдены. Попробуйте снова.",
                reply_markup=notes_menu(has_notes)
            )
    except ValueError:
        bot.send_message(
            message.chat.id,
            "⚠️ Ошибка: введите индексы в правильном формате (например: 0,2,4).",
            reply_markup=notes_menu(has_notes=True)
        )


@bot.message_handler(func=lambda msg: msg.text == "⬅️ Назад")
def back_to_main_menu(message):
    bot.send_message(
        message.chat.id,
        "Вы вернулись в главное меню. Выберите категорию:",
        reply_markup=main_menu()
    )


if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
