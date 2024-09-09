import telebot
from telebot import types
import psycopg2

token = '6741751858:AAHPRaRZFuRFetyeVpI04aAH6vQEaaiDguc'
bot = telebot.TeleBot(token)
data = ['спасибо', 'привет', 'сессия']
db = psycopg2.connect(database="polytech_db", user="postgres", password="VArth123")
cur = db.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Хочу", "/help", "/timetable")
    bot.send_message(message.chat.id,
                     'Здравствуйте! Хотите узнать свежую информацию о Мосполитех или получить свежую информацию о расписании?',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Я бот с расписанием\n'
                                      'Доступные команды:\n'
                                      '/start - выход в главное меню\n'
                                      '/lms_polytech - ссылка на сайт Мосполитеха c курсами\n'
                                      '/timetable - Информация о расписании')


@bot.message_handler(func=lambda message: message.text == "Хочу")
def answer(message):
    bot.send_message(message.chat.id, 'Тогда тебе сюда: https://mospolytech.ru/')


@bot.message_handler(commands=['lms_polytech'])
def url(message):
    bot.reply_to(message, "Ссылка на сайт СДО Московского политехнического университета:\n"
                          "https://online.mospolytech.ru/")


@bot.message_handler(commands=['timetable'])
def pari(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Понедельник📆", "Вторник📆", "Среда📆")
    keyboard.row("Четверг📆", "Пятница📆", "Суббота📆")
    keyboard.row("Расписание на неделю🗓")
    bot.reply_to(message, "На какой день недели тебя интересует расписание?", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Расписание на неделю🗓")
def week(message):
    # Здесь вы должны выполнить запрос к базе данных
    request = 'SELECT a.day_of_week, name, room_num, start_time, full_name FROM timetable a JOIN subject b ON a.subject_id = b.subject_id JOIN teacher c ON b.subject_id = c.subject_id'
    cur.execute(request)  # Выполнение запроса
    abv = cur.fetchall()  # Получение всех результатов
    if len(abv) > 0:  # Если есть результаты
        abv_text = ""
        for i in abv:
            # Предполагается, что i[0] - это день недели, i[1] - название предмета, и т.д.
            if i[0] not in abv_text:
                abv_text += f"\n*{i[0]}*📆:\n"  # Добавить день недели
            abv_text += f"_{i[1]}_ \n {i[2]}\n 🕘{i[3]} \n👤{i[4]}\n\n"
        bot.send_message(message.chat.id, abv_text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, 'Расписание не найдено')


@bot.message_handler(
    func=lambda message: message.text in ["Понедельник📆", "Вторник📆", "Среда📆", "Четверг📆", "Пятница📆", "Суббота📆"])
def den(message):
    day = message.text.strip("📆")  # Получаем выбранный день недели из текста сообщения
    # Включаем день недели в запрос SQL, используя параметризованный запрос для предотвращения SQL инъекций
    request = ('SELECT a.day_of_week, b.name, a.room_num, a.start_time, c.full_name '
               'FROM timetable a '
               'JOIN subject b ON a.subject_id = b.subject_id '
               'JOIN teacher c ON b.subject_id = c.subject_id '
               'WHERE a.day_of_week = %s')  # %s будет заменен на значение переменной day
    cur.execute(request, (day,))  # Выполнение запроса с днем недели в качестве параметра
    abv = cur.fetchall()  # Получение всех результатов
    if len(abv) > 0:  # Если есть результаты
        abv_text = f"*{day}*📆:\n\n"
        for i in abv:
            # Добавляем информацию о каждом занятии
            subject = i[1]
            room_num = i[2]
            start_time = i[3]
            full_name = i[4]
            abv_text += f"_{subject}_\n {room_num}\n 🕘{start_time} \n👤{full_name} \n\n"
        bot.send_message(message.chat.id, abv_text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "На выбранный день расписание отсутсвует")


@bot.message_handler(content_types=['text'])
def pechat(message):
    if message.text.lower() == data[0]:
        bot.send_message(message.chat.id, 'Рад был вам помочь!')
    elif message.text.lower() == data[1]:
        bot.send_message(message.chat.id, 'Здравствуйте, ' + message.from_user.first_name + ', о командах /help')
    elif message.text.lower() == data[2]:
        bot.send_message(message.chat.id,
                         'Извините, но расписание о сессии еще находится на стадии разработки. Скоро обязательно все сделаем')
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял.')


bot.polling()
