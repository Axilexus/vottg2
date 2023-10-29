from pyrogram import Client, filters
from pyrogram.types import Message
import sqlite3
from config import api_id, api_hash
# Создаем подключение к базе данных

# Получаем все атрибуты модуля filters
functions = [attr for attr in dir(filters) if callable(getattr(filters, attr))]

# Выводим список функций
for function in functions:
    print(function)

app = Client('my_bot2', api_id=api_id, api_hash=api_hash)

# Функция для вывода расписания
@app.on_message(filters.command("r"))
def show_schedule(_, message: Message):
    conn = sqlite3.connect('schedule33.db')
    cursor = conn.cursor()
    # Создаем таблицу для хранения расписания
    cursor.execute('''CREATE TABLE IF NOT EXISTS schedule  (day text, subjects text)''')
    conn.commit()
    # Получаем расписание из базы данных
    cursor.execute("SELECT * FROM schedule")
    rows = cursor.fetchall()

    # Формируем сообщение с расписанием
    schedule_message = "🖥️ Расписание на Текущую неделю:\n\n"
    days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]

    for day in days:
        schedule_message += f"{day}: "
        subjects = [row[1] for row in rows if row[0] == day]
        if subjects:
            schedule_message += ", ".join(subjects)
        else:
            schedule_message += "пока что ничего нет."
        schedule_message += "\n\n"

    # Отправляем сообщение с расписанием
    message.reply_text(schedule_message)
    conn.close()

# Функция для записи предметов в базу данных
@app.on_message(filters.command("add"))
def add_subjects(_, message: Message):
    conn = sqlite3.connect('schedule33.db')
    cursor = conn.cursor()
    # Создаем таблицу для хранения расписания, если она еще не создана
    cursor.execute('''CREATE TABLE IF NOT EXISTS schedule (day text, subjects text)''')
    conn.commit()
    # Получаем день и предметы из сообщения
    command, day, *subjects = message.text.split()
    # Удаляем записи для указанного дня из таблицы
    cursor.execute("DELETE FROM schedule WHERE day=?", (day,))
    conn.commit()
    # Записываем предметы в базу данных
    for subject in subjects:
        cursor.execute("INSERT INTO schedule VALUES (?, ?)", (day, subject))
    conn.commit()
    # Отправляем подтверждение
    message.reply_text("Предметы успешно добавлены в расписание!")
    conn.close()

@app.on_message(filters.pinned_message)
def handle_pinned_message(client, message):
    # Получаем идентификаторы пользователей, которые закрепили и написали сообщение
    pinned_by_user_id = message.from_user.id
    author_user_id = message.pinned_message.from_user.id

    # Получаем имена пользователей
    pinned_by_user_name = message.from_user.first_name
    author_user_name = message.pinned_message.from_user.first_name

    # Проверяем, что закрепленное сообщение содержит текст
    if message.pinned_message.text:
        # Формируем текст для отправки
        text = f"Закрепленное сообщение от {author_user_name}:\n\n{message.pinned_message.text}\n\nЗакрепил: {pinned_by_user_name}"

        # Отправляем содержимое закрепленного сообщения с именами пользователей
        client.send_message(
            chat_id=message.chat.id,
            text=text
        )
# Флаг для определения состояния цикла
is_running = False



# Функция для вывода расписания
@app.on_message(filters.command("h"))
def show_homework(_, message: Message):
    conn = sqlite3.connect('homework.db')
    cursor = conn.cursor()
    # Создаем таблицу для хранения расписания
    cursor.execute('''CREATE TABLE IF NOT EXISTS schedule  (day text, subjects text)''')
    conn.commit()
    # Получаем расписание из базы данных
    cursor.execute("SELECT * FROM schedule")
    rows = cursor.fetchall()

    # Формируем сообщение с расписанием
    schedule_message = "🖥️ ДЗ на следующий урок:\n\n"
    days = ["Математика", "Русский", "Литература", "История", "ОБЖ", "Английский", "Обществознание", "Немецкий", "Информатика", "Физика", "Биология", "Химия", "География", "ИП", "Нач.Проект.ЭПиУ"]

    for day in days:
        schedule_message += f"{day}: "
        subjects = [row[1] for row in rows if row[0] == day]
        if subjects:
            schedule_message += ", ".join(subjects)
        else:
            schedule_message += "пока что ничего нет."
        schedule_message += "\n\n"

    # Отправляем сообщение с расписанием
    message.reply_text(schedule_message)
    conn.close()

# Функция для записи предметов в базу данных
@app.on_message(filters.command("addh"))
def add_homework(_, message: Message):
    conn = sqlite3.connect('homework.db')
    cursor = conn.cursor()
    # Создаем таблицу для хранения расписания, если она еще не создана
    cursor.execute('''CREATE TABLE IF NOT EXISTS schedule (day text, subjects text)''')
    conn.commit()
    # Получаем день и предметы из сообщения
    command, day, *subjects = message.text.split()
    # Удаляем записи для указанного дня из таблицы
    cursor.execute("DELETE FROM schedule WHERE day=?", (day,))
    conn.commit()
    # Записываем предметы в базу данных
    for subject in subjects:
        cursor.execute("INSERT INTO schedule VALUES (?, ?)", (day, subject))
    conn.commit()
    # Отправляем подтверждение
    message.reply_text("Задание успешно добавлены в список")
    conn.close()



# Функция обработки команды /s
@app.on_message(filters.command("s"))
def start_loop(client, message):
    global is_running
    if not is_running:
        is_running = True
        message.reply_text("Цикл запущен.")
        run_loop(client, message.chat.id)

# Функция обработки команды /t
@app.on_message(filters.command("t"))
def stop_loop(client, message):
    global is_running
    if is_running:
        is_running = False
        message.reply_text("Цикл остановлен.")

# Функция, выполняющаяся в цикле
def run_loop(client, chat_id):
    global is_running
    while is_running:
        # Действия, выполняемые в цикле
        client.send_message(chat_id, "Саси")
@app.on_message(filters.command("addv", prefixes="/"))
def add_voice_message(client, message):
    conn = sqlite3.connect("voice_messages1.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voice_messages1 (
        name TEXT PRIMARY KEY,
        file_id TEXT,
        user_id INTEGER,
        first_name TEXT,
        last_name TEXT
    )
""")
    if message.reply_to_message and message.reply_to_message.voice:
        name = message.text.split(maxsplit=1)[1]
        file_id = message.reply_to_message.voice.file_id
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        last_name = message.reply_to_message.from_user.last_name

        cursor.execute("""
            INSERT OR REPLACE INTO voice_messages1 (name, file_id, user_id, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        """, (name, file_id, user_id, first_name, last_name))
        conn.commit()
        m=client.send_message(message.chat.id, "Voice message added successfully!")
    else:
        m=client.send_message(message.chat.id, "Reply to a voice message to add it with a name.")
    message.delete()
    m.delete()
@app.on_message(filters.command("v", prefixes="/"))
def send_voice_message_names(client, message):
    conn = sqlite3.connect("voice_messages1.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voice_messages1 (
        name TEXT PRIMARY KEY,
        file_id TEXT,
        user_id INTEGER,
        first_name TEXT,
        last_name TEXT
    )
""")
    cursor.execute("SELECT name FROM voice_messages1")
    rows = cursor.fetchall()
    names = "\n".join([row[0] for row in rows])
    client.send_message(message.chat.id, f"Voice message names:\n{names}")
    message.delete()

@app.on_message(filters.command("d", prefixes="/"))
def send_voice_message(client, message):
    conn = sqlite3.connect("voice_messages1.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voice_messages1 (
        name TEXT PRIMARY KEY,
        file_id TEXT,
        user_id INTEGER,
        first_name TEXT,
        last_name TEXT
    )
""")
    command, name = message.text.split(maxsplit=1)
    cursor.execute("SELECT file_id FROM voice_messages1 WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        file_id = row[0]
        client.send_voice(message.chat.id, file_id)
    else:
        m = client.send_message(message.chat.id, "Invalid voice message name")
    message.delete()
    m.delete()
        
@app.on_message(filters.command("rmv", prefixes="/"))
def remove_voice_message(client, message):
    conn = sqlite3.connect("voice_messages1.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voice_messages1 (
        name TEXT PRIMARY KEY,
        file_id TEXT,
        user_id INTEGER,
        first_name TEXT,
        last_name TEXT
    )
""")
    command, name = message.text.split(maxsplit=1)
    cursor.execute("DELETE FROM voice_messages1 WHERE name = ?", (name,))
    conn.commit()
    m = client.send_message(message.chat.id, "Voice message removed successfully!")
    message.delete()
    m.delete()
@ app.on_message(filters.command("zv", prefixes="/"))
def send_photo(client, message):
    # Путь к файлу с заготовленным фото
    photo_path = "zvonok.jpg"

    # Отправляем фото
    client.send_photo(
        chat_id=message.chat.id,
        photo=photo_path,
        caption="Расписание звонков"
    )
@app.on_message(filters.command(["save_photo"], prefixes="/"))
def save_photo(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo.file_id
        file_path = client.download_media(photo)  # Сохраняем фото на сервере
        message.reply_text(f"Фото сохранено: {file_path}")
    else:
        message.reply_text("Ответьте на фото, чтобы сохранить его.")

# Запускаем клиент Pyrogram
app.run()
