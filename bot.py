import telebot
import config
from DataBase.database import DataBase

bot = telebot.TeleBot(config.TOKEN)
database = DataBase(
    db_user = config.DB_USER,
    db_password = config.DB_PASSWORD,
    db_name = config.DB_NAME,
)

@bot.message_handler(commands=['start'])
def send_start_message(message):
    database.register_user(message)
    bot.send_message(message.chat.id, 'Какое-то стартовое сообщение')

@bot.message_handler(commands=['sub'])
def send_sub(message):
    database.subscribe_user(message)
    bot.send_message(message.chat.id, 'Ты подписан')

@bot.message_handler(commands=['sub'])
def send_unsub(message):
    database.unsubscribe_user(message)
    bot.send_message(message.chat.id, 'Ты отписан, лох')

@bot.message_handler(commands=['get_all_users_identificators'])
def test1(message):
    msg = ' '.join(map(str, database.get_all_users_identificators()))
    bot.send_message(message.from_user.id, msg)

@bot.message_handler(commands=['get_all_users'])
def test2(message):
    msg = ' '.join(map(str, database.get_all_users()))
    bot.send_message(message.from_user.id, msg)

bot.polling(none_stop=True)