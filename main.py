import sys
import telebot
import settings
import core
from flask import Flask, request

app = Flask(__name__)

bot = telebot.TeleBot(settings.BOT_TOKEN, threaded=False)

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard.row('🖨 Катридж', '🖥 Периферія')
keyboard.row('📈 Статистика', '📊 Рейтинг')


@bot.message_handler(commands=['start'])
def start_handler(message):

    if message.chat.id == 207488122:
        s = '<b>{}</b>, Знову ти?'.format(message.chat.first_name)
        bot.send_message(message.chat.id, s, parse_mode='HTML')
        return

    msg = 'Хай, {} 😊. Вот тобі менюшка, працюй!)'.format(message.chat.first_name)

    bot.send_message(chat_id=message.chat.id, text=msg, parse_mode='HTML', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def main_menu(message):

    if message.chat.id == 207488122:
        s = '<b>{}</b>, Знову ти?'.format(message.chat.first_name)
        bot.send_message(message.chat.id, s, parse_mode='HTML')
        return

    name = message.chat.first_name + ' ' + (message.chat.last_name or '')

    core.log(message.chat, message.text)

    if message.text == '🖨 Катридж':

        msg = 'Плюс катридж!'

        core.add_points(message.chat.id, message.chat.username, name, 'Катридж', 1)

    elif message.text == '🖥 Периферія':

        msg = 'Плюс периферія!'

        core.add_points(message.chat.id, message.chat.username, name, 'Периферія', 2)

    elif message.text == '📈 Статистика':

        msg = core.get_user_stat_by_id(message.chat.id)

    elif message.text == '📊 Рейтинг':

        msg = core.get_ranking()

    else:

        msg = 'Не розумію'

    bot.send_message(message.chat.id, msg, reply_markup=keyboard, parse_mode='HTML')


@app.route('/hello')
def route_hello():

    return 'Hello world!'


@app.route(settings.WEBHOOK_PATH, methods=['POST', 'GET'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])

    return "!", 200


def main_pooling():

    core.log(m='Запуск сервера')
    bot.polling(none_stop=True)


def main_webhook():

    core.log(m='Встановлено вебхук')
    bot.set_webhook(settings.WEBHOOK_URL + settings.WEBHOOK_PATH, max_connections=1)


core.create_user_stats_table_if_not_exists()
if __name__ == "__main__":
    main_pooling()
else:
    main_webhook()



