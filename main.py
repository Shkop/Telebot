import telebot
import requests
import json

from extensions import APIException, Convertor
from config import *
import traceback



bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = """Приветствуем Вас в нашем обменном пункте! Чтобы начать работу, введите команду в следующем формате:
           <имя валюты><в какую валюту перевести><количество переводимой валюты>
           <Также можно провести конвертацию пошагово с помощью команды: /convert>
           <Узнать список валют можно с помощью команды /values>"""
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text='Выберите валюту которую хотите обменять:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text='Выберите валюту которую хотите получить:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, sym_handler, base)


def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text='Выберите количество получаемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        new_price=Convertor.get_price(base, sym, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации \n{e}")
    else:
        text = f'Цена {amount} {base} {sym} : new_price'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)



bot.polling(none_stop=True)