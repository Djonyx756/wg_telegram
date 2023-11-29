import telebot
from telebot import types # для указание типов
import time
import datetime
import subprocess
import sys
import os
#from config import *
config = ""
# Создаем экземпляр бота
bot = telebot.TeleBot('api telegram')

def save_config(message):
    global config
    config = message.text
    print("----------------")
    print(config)
    print("----------------")
    string = str(config)
    bot.send_message(message.chat.id, "Настройки конфигурации сохранены")
    return string

def del_vpn(message):
    config_string = message.text
    subprocess.run(['scripts/del_cl.sh', config_string])
    bot.send_message(message.chat.id, f"IP-адрес 10.10.0.{config_string} успешно удален.")

def add_vpn(message):
    config_string = message.text
    subprocess.run(['scripts/add_cl.sh', config_string])
    bot.send_message(message.chat.id, f"Конфиг {config_string}.conf создан")

    config_file_path = f"/etc/wireguard/{config_string}_cl.conf"
    with open(config_file_path, 'rb') as file:
        bot.send_document(message.chat.id, file)
    bot.send_message(message.chat.id, "Конфигурационный файл успешно отправлен.")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1q = types.KeyboardButton("👋 MONITOR!")
    btn2q = types.KeyboardButton("ADMIN")
    markup.add(btn1q, btn2q)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! управления VPN Wireguard".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=["id"])
def id(message):
    bot.send_message(message.chat.id, text="Id :"+str(message.chat.id)+"\nuername :"+str(message.from_user.username))
    print(str(message.chat.id))

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "👋 MONITOR!"):
        bot.send_message(message.chat.id, text="Здесь мониторинг vpn сервера")
        if (1==1):
            bot.send_message(message.chat.id, text="Привет хозяин")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            botton32 = types.KeyboardButton("STATUS")
            botton42 = types.KeyboardButton("Dell VPN")
            botton41 = types.KeyboardButton("Add VPN")
            botton43 = types.KeyboardButton("STOP")
            back = types.KeyboardButton("Back")
            markup.add(botton32, botton41, botton42, botton43, back)
            bot.send_message(message.chat.id, text="Выполни запрос", reply_markup=markup)
    elif(message.text == "ADMIN"):
        if (1==1):
            bot.send_message(message.chat.id, text="Привет хозяин")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            botton22 = types.KeyboardButton("WG FIRST START")
            back = types.KeyboardButton("Back")
            markup.add(botton22, back)
            bot.send_message(message.chat.id, text="Выполни запрос", reply_markup=markup)
    elif message.text == "Dell VPN":
        bot.send_message(message.chat.id, "Введите ip, который нужно удалить:")
        bot.register_next_step_handler(message, del_vpn)
    elif message.text == "Add VPN":
#        subprocess.run(['scripts/add_cl.sh'])
#        bot.send_message(message.chat.id, "Введите настройки конфигурации:")
#        bot.register_next_step_handler(message, save_config)
        bot.send_message(message.chat.id, "Введите название нового конфига")
        bot.register_next_step_handler(message, add_vpn)
    elif (message.text == "Back"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 MONITOR!")
        button2 = types.KeyboardButton("ADMIN")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Back", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")
    message_text = message.text
    print(message_text)

bot.polling(none_stop=True)
