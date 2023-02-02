import requests
from datetime import datetime
import telebot
from telebot import types
# create file data_token with variable: token = "your token tg bot"
from data_token import token, token_w, city

    # creating tg bot.


def telegram_bot(token, token_w, city):
    bot = telebot.TeleBot(token)

    # welcome and show all bot commands.
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_commands = types.KeyboardButton('Show my commands')
        markup.add(btn_commands)
        bot.send_message(message.chat.id, "welcome to UnotunoBOT", reply_markup=markup)

    # rate usd
    @bot.message_handler(commands=['rate'])
    def rate(message):
        bot.send_message(message.chat.id, 'You wanna to know actual rate? Y/N')
    # weather
    @bot.message_handler(commands=['weather'])
    def weather(message):
        bot.send_message(message.chat.id, 'Write Your city (gomel)')
    # create buttons.
    @bot.message_handler(commands=['button'])
    def info_buttons(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_author = types.KeyboardButton('About author')
        btn_git = types.KeyboardButton('My GitHub link')
        btn_tg = types.KeyboardButton('My Telegram link')
        markup.add(btn_author, btn_git, btn_tg)
        bot.send_message(message.chat.id, 'Choose a button', reply_markup=markup)

    # all bot answers
    @bot.message_handler(content_types=['text'])
    def send_msg(message):
        # block rate request
        if message.text.lower() == 'y':
            try:
                req = requests.get("https://www.nbrb.by/api/exrates/rates/431")
                response = req.json()
                cur_rate = response["Cur_OfficialRate"]
                bot.send_message(message.chat.id, (
                    f"{datetime.now().strftime('%d - %m %H:%M')}\nКурс 1 доллара на текущий момент {cur_rate} BYN"))
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, "Houston we have a problem")
        # bot reaction
        elif message.text.lower() == 'n':
            bot.send_message(message.chat.id, 'Ok. See you later')
        elif message.text == 'Show my commands':
            bot.send_message(message.chat.id, '/rate , /weather , /button')
        elif message.text == 'About author':
            bot.send_message(message.chat.id,
                             'My name is Sergey, 32 years old living in Belarus, Gomel city. I need some pet-projects for my exp. Thanks.')
        elif message.text == 'My GitHub link':
            bot.send_message(message.chat.id, '[https://github.com/iamkape]')
        elif message.text == 'My Telegram link':
            bot.send_message(message.chat.id, '[https://t.me/unotuno]')

        # weather block request

        elif message.text.lower() == 'gomel':
            try:
                req = requests.get(
                    f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token_w}&units=metric')
                response = req.json()
                temp = response['main']['temp']
                temp_feels = response['main']['feels_like']
                w_speed = response['wind']['speed']
                clouds = response['clouds']['all']
                bot.send_message(message.chat.id, (
                    f'Air temperature is {round(temp)}, feels like {round(temp_feels)}, with wind speed  {w_speed} m/s, clouds {clouds}%'
                ))
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, "Houston we have a problem")
        else:
            bot.send_message(message.chat.id, "I don't know that command")
    bot.polling(none_stop=True)


if __name__ == "__main__":
    telegram_bot(token, token_w, city)