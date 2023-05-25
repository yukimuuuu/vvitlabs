from datetime import date, timedelta
import telebot
from telebot import types
import psycopg2

conn = psycopg2.connect(database="vvitlab7",
                        user="postgres",
                        password="mvpe86qw",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

st = 0

token = '5992581657:AAEajCk6jxzNhuyPeeZ3Tnn5u_zoq38mII0'
bot = telebot.TeleBot(token)


def get_schedule(text2, qweek, message):
    cursor.execute("SELECT * "
                   "FROM schedule "
                   "WHERE lower(day)=lower(%s) and lower(week) =lower(%s)", (str(text2), str(qweek)))
    schedule = cursor.fetchall()
    if not schedule:
        text = "[" + str.title(text2) + "]\n" + 'В этот день нет пар.\n'
    else:
        text = "[" + str.title(text2) + "]\n"
        for row in schedule:
            text += str(row[1]) + ' ' + str(row[2]) + ' ' + str(row[3]) + '\n'
    return text


@bot.message_handler(commands=['start'])
def start(message):
    global st
    if st == 0:
        st = 1
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row("Понедельник")
        keyboard.row("Вторник", "Среда")
        keyboard.row("Четверг", "Пятница")
        keyboard.row("На текущую неделю")
        keyboard.row("На следующую неделю")
        bot.send_message(message.from_user.id, "Добрый день!\nХотите узнать расписание?\n\n"
                                               "Подробнее о доступных командах /help", reply_markup=keyboard)


@bot.message_handler(commands=['menu'])
def start(message):
    if st == 1:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row("Понедельник")
        keyboard.row("Вторник", "Среда")
        keyboard.row("Четверг", "Пятница")
        keyboard.row("На текущую неделю")
        keyboard.row("На следующую неделю")
        bot.send_message(message.from_user.id, "Хотите узнать расписание?\n\n"
                                                   "Подробнее о доступных командах /help", reply_markup=keyboard)


@bot.message_handler(commands=['mtuci'])
def start(message):
    if st == 1:
        a = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Официальный сайт МТУСИ. /menu\nhttps://mtuci.ru/", reply_markup=a)


@bot.message_handler(commands=['help'])
def start(message):
    if st == 1:
        a = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Список доступных команд:\n/menu - вернуться в меню"
                                               "\n/week - узнать значение текущей недели"
                                               "\n/mtuci - информация о нашем вузе", reply_markup=a)


@bot.message_handler(commands=['week'])
def start(message):
    if st == 1:
        delta = date.today() - date(2023, 5, 15)
        if int(delta / timedelta(days=7)) % 2 == 0:
            a = types.ReplyKeyboardRemove()
            bot.send_message(message.from_user.id, 'Сейчас идет четная неделя. /menu', reply_markup=a)
        else:
            a = types.ReplyKeyboardRemove()
            bot.send_message(message.from_user.id, 'Сейчас идет нечетная неделя. /menu', reply_markup=a)


@bot.message_handler(content_types=['text'])
def answer(message):
    text = message.text.lower()
    q = ''
    if text in ('понедельник', 'вторник', 'среда', 'четверг', 'пятница'):
        delta = date.today() - date(2023, 5, 15)
        if int(delta / timedelta(days=7)) % 2 == 0:
            qweek = 'Четная'
        else:
            qweek = 'Нечетная'
        a = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, get_schedule(text, qweek, message) + "/menu", reply_markup=a)
    elif text == 'на следующую неделю':
        delta = date.today() - date(2023, 5, 15)
        if int(delta / timedelta(days=7)) % 2 == 0:
            qweek = 'Нечетная'
        else:
            qweek = 'Четная'
        for i in ('понедельник', 'вторник', 'среда', 'четверг', 'пятница'):
            q += get_schedule(i, qweek, message)
        a = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, q + "/menu", reply_markup=a)
    elif text == 'на текущую неделю':
        delta = date.today() - date(2023, 5, 15)
        if int(delta / timedelta(days=7)) % 2 == 0:
            qweek = 'Четная'
        else:
            qweek = 'Нечетная'
        for i in ('понедельник', 'вторник', 'среда', 'четверг', 'пятница'):
            q += get_schedule(i, qweek, message)
        a = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, q + "/menu", reply_markup=a)
    else:
        a = types.ReplyKeyboardRemove()
        print(text)
        bot.send_message(message.chat.id, 'Извините, я вас не понял. /menu', reply_markup=a)

bot.polling(none_stop=True)
