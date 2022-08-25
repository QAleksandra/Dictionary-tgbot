# В google colab добавить: !pip install pyTelegramBotAPI

import telebot
from telebot import types
import json

bot = telebot.TeleBot(token='Вставьте токен ', parse_mode='html')

with open('dict.json', "r", encoding="utf-8") as json_file:
    DEFINITIONS = json.load(json_file)

listDEFINITIONS = list(DEFINITIONS.values())

newDEFINITIONS = []

@bot.message_handler(commands=['start'])
def start_command_handler(message):
    sti = open('welcome.jpg', 'rb')
    bot.send_sticker(message.chat.id, sti)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Кому это пришло в голову? 🌚')
    markup.add(item1)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!\nЯ — бот, который придёт на помощь, когда ты встретишь в работе страшные и незнакомые английские слова 👨🏻‍💻 \nОтправь мне интересующее тебя слово, а я покажу его перевод!", parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_handler(message):
    definition = DEFINITIONS.get(message.text.lower())
    if definition is not None and message.text != "Кому это пришло в голову? 🌚":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Кому это пришло в голову? 🌚')
        markup.add(item1)
        bot.send_message(message.chat.id, text=f'Определение:\n<code>{definition}</code>')
        bot.send_message(message.chat.id, text=f'Переведём ещё что-нибудь?', reply_markup=markup)

    elif message.text == "Кому это пришло в голову? 🌚":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Сайт-визитка', url='https://qaleksandra.github.io/CV/')
        markup.add(button1)
        bot.send_message(message.chat.id, 'Переходи по ссылке и узнаешь ;)'.format(message.from_user), reply_markup=markup)

    elif definition is None and message.text != "Кому это пришло в голову? 🌚":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Кому это пришло в голову? 🌚')
        markup.add(item1)
        newDEFINITIONS.append(message.text)
        with open('newdict.txt', "a", encoding="utf-8") as txt_file:
            print(*newDEFINITIONS, file=txt_file, sep="\n")
        bot.send_message(message.chat.id, f'О, я смотрю вы из Англии... 💂🏻 А я — нет, придётся записать <u><b>{message.text}</b></u> к себе ✏️', reply_markup=markup)

def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
