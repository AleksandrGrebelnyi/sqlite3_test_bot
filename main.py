import telebot
# import conf
import sqlite3  # импортируем и будем делать БД с помощью sqlite3

# bot
bot = telebot.TeleBot('TOKEN', parse_mode='HTML')
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
    if message.chat.id == MY_ID:  # если ставить например мой id значит только я смогу делать рассылку
        try:
            for user in all_id:
                bot.send_message(*list(map(int, user)), message.text)
            connect.commit()
        except Exception as ex:
            print(ex, 'bot was deleted')
            cursor.execute(f"DELETE FROM us_id")


# polling
bot.polling(none_stop=True)
