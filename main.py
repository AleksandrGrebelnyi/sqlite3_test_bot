import requests
from flask import Flask, request
import telebot
import os
import sqlite3

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
MY_ID = os.environ.get('MY_ID')
# bot
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')
user_info = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    connect = sqlite3.connect('users.db')  # создали файл
    cursor = connect.cursor()  # курсор для взаимодействия с users.db

    cursor.execute("""CREATE TABLE IF NOT EXISTS us_id(
        id INTEGER
    )""")  # создаем таблицу в которой будут id пользователей
    connect.commit()

    # check есть ли уже такой id в нашем us_id
    client_id = message.chat.id
    cursor.execute(f"SELECT id FROM us_id WHERE id = {client_id}")
    data = cursor.fetchone()  # все поля с id
    if data is None:
        # add инфо
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO us_id VALUES(?);", user_id)
        connect.commit()
    # else: возможно дописать что то

# если пользователь заблочил бота, чистим БД
# @bot.message_handler(commands=['delete'])
# def delete(message):
#     connect = sqlite3.connect('users.db')  # создали файл
#     cursor = connect.cursor()
#     select_query = """SELECT * from us_id"""
#     cursor.execute(select_query)  # "SELECT * FROM us_id"
#     all_id = cursor.fetchall()
#     if message.chat.id == 467142471:
#         try:
#             for user in all_id:
#                 bot.send_message(*list(map(int, user)), message.text)
#             connect.commit()
#         except Exception as ex:
#             print(ex, 'bot was deleted')
#             cursor.execute(f"DELETE FROM us_id")
#             connect.commit()

@bot.message_handler(commands=['ad'])
def ad(message):
    connect = sqlite3.connect('users.db')  # создали файл
    cursor = connect.cursor()
    print('Switch on')
    # client_id = message.from_user.id
    select_query = """SELECT * from us_id"""
    cursor.execute(select_query)  # "SELECT * FROM us_id"
    all_id = cursor.fetchall()
    print(f'Number of strings: {len(all_id)}')
    print(f'Display every string ')
    if message.chat.id == MY_ID:
        try:
            for user in all_id:
                bot.send_message(*list(map(int, user)), message.text)
            connect.commit()
        except Exception as ex:
            print(ex, 'bot was deleted')
            cursor.execute(f"DELETE FROM us_id")

    # for user in user_info:
    #     bot.send_message(user, message.text[message.text.find(' '):])

# print(user_info)
# print(type(user_info))

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Python Telegram Bot", 200


@app.route('/')
def main():
    bot.remove_webhook()
    bot.set_webhook(url='https://telega2bot.herokuapp.com/' + TOKEN)
    return 'Python Telegram Bot', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
# polling
# bot.polling(none_stop=True)
