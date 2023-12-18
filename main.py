import telebot
from telebot import types # для указание типов
import time
import datetime
import subprocess
import sys
import os
import glob
import qrcode
from config import *
#from config import *
config = ""
# Создаем экземпляр бота
bot = telebot.TeleBot(api_tg)

def save_config(message):
    global config
    config = message.text
    print("----------------")
    print(config)
    print("----------------")
    string = str(config)
    bot.send_message(message.chat.id, "Настройки конфигурации сохранены")
    return string

def qr(name_qr, chat_id):
    # Чтение содержимого файла
    with open(name_qr, 'r') as file:
        text = file.read()
    # Создание объекта QR-кода
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    # Создание изображения QR-кода
    img = qr.make_image(fill_color='black', back_color='white')
    # Сохранение изображения в файл
    img_path = "my_qrcode.png"
    img.save("my_qrcode.png")
    # Отправка QR-кода через Telegram бота
    with open(img_path, 'rb') as f:
        bot.send_photo(chat_id=chat_id, photo=f)
    # Удаление QR-кода
    os.remove(img_path)

def check_message(message):
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!? ')
    new_message = ''.join(c if c in valid_chars else '_' for c in message)
    new_message = new_message.replace(' ', '_')
    return new_message.lower().strip()

def check_number_in_range(number):
    try:
        num = int(number)
        if 2 <= num <= 253:
            return True
        else:
            return False
    except ValueError:
        return False

def buttons(message):
#    bot.send_message(message.chat.id, text="Привет хозяин")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    botton32 = types.KeyboardButton("Конфиги")
    botton42 = types.KeyboardButton("Удалить_конфиг")
    botton41 = types.KeyboardButton("Добавить_конфиг")
    back = types.KeyboardButton("Назад")
    markup.add(botton32, botton41, botton42, back)
    bot.send_message(message.chat.id, text="Выполни запрос", reply_markup=markup)

def del_vpn(message):
    if message.sticker is not None:
        # Если пользователь отправил стикер вместо текста
        bot.reply_to(message, 'Пожалуйста, отправьте текстовое сообщение, а не стикер.')
        buttons(message)
    elif message.voice is not None:
        bot.reply_to(message, 'Пожалуйста, отправьте текстовое сообщение, а не голосовое сообщение.')
        buttons(message)
    elif message.document is not None:
        bot.reply_to(message, 'Пожалуйста, отправьте текстовое сообщение, а не документ.')
        buttons(message)
    else:
        # Обработка текстового сообщения
        bot.reply_to(message, 'Вы отправили текстовое сообщение.')
        config_string = check_message(message.text)
        if check_number_in_range(message.text):
            subprocess.run(['scripts/del_cl.sh', config_string])
            script_path = os.path.dirname(os.path.realpath(__file__))
            rm_user_script = os.path.join(script_path, "rm_user.sh")
            subprocess.run([rm_user_script, config_string])
            bot.send_message(message.chat.id, f"IP-адрес 10.10.0.{config_string} успешно удален.")
            print(f"{message.text} находится в допустимом диапазоне.")
        else:
            print(f"{message.text} не находится в допустимом диапазоне.")
            bot.send_message(message.chat.id, f"IP-адрес 10.10.0.{config_string} не может быть удален. Ввведите число от 2 до 253")
    buttons(message)



def add_vpn(message):
    if message.chat.id in mainid:
#        bot.send_message(message.chat.id, text="Привет избранный!!")
        if message.sticker is not None:
            # Если пользователь отправил стикер вместо текста
            bot.reply_to(message, 'Пожалуйста, отправьте текстовое сообщение, а не стикер.')
            buttons(message)
        elif message.voice is not None:
            bot.reply_to(message, 'Пожалуйста, отправьте текстовое сообщение, а не голосовое сообщение.')
            buttons(message)
        elif message.document is not None:
            bot.reply_to(message, 'Пожалуйста, отправьте текстовое сообщение, а не документ.')
            buttons(message)
        else:
            # Обработка текстового сообщения
#            bot.reply_to(message, 'Вы отправили текстовое сообщение.')
            config_string = check_message(message.text)
            subprocess.run(['scripts/add_cl.sh', config_string])
            bot.send_message(message.chat.id, f"Конфиг {config_string}.conf создан")
            config_file_path = f"/etc/wireguard/{config_string}_cl.conf"
            qr(config_file_path, message.chat.id)
            with open(config_file_path, 'rb') as file:
                bot.send_document(message.chat.id, file)
            with open(config_file_path, 'r') as file:
                config_content = file.read()
            bot.send_message(message.chat.id, config_content)
            bot.send_message(message.chat.id, "Конфигурационный файл успешно отправлен.")
            buttons(message)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in mainid:
#        bot.send_message(message.chat.id, text="Привет избранный!!")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1q = types.KeyboardButton("Мониторинг")
        btn2q = types.KeyboardButton("Администрирование")
        markup.add(btn1q, btn2q)
        bot.send_message(message.chat.id, text="{0.first_name}, добро пожаловать в бот управления VPN Wireguard".format(message.from_user), reply_markup=markup)
    elif(str(message.chat.id) != mainid):
        bot.send_message(message.chat.id, text="Привет, {0.first_name}! Ты заплутал!!".format(message.from_user))

@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    # Обработка сообщения со стикером
    bot.reply_to(message, 'Вы отправили стикер!')

@bot.message_handler(commands=["id"])
def id(message):
    bot.send_message(message.chat.id, text="Id :"+str(message.chat.id)+"\nusername :"+str(message.from_user.username))
    print(str(message.chat.id))

@bot.message_handler(content_types=['text'])
def func(message):
    if message.chat.id in mainid:
#        bot.send_message(message.chat.id, text="Привет избранный!!")
        formatted_message = check_message(message.text)
        print(formatted_message)
        if not formatted_message:  # Проверяем, что сообщение не пустое
            return
        if(message.text == "Мониторинг"):
#            bot.send_message(message.chat.id, text="Здесь мониторинг vpn сервера")
            buttons(message)
        elif(message.text == "Администрирование"):
            if (1==1):
#                bot.send_message(message.chat.id, text="Привет хозяин")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                botton22 = types.KeyboardButton("Установка_Wireguard")
                botton_reset = types.KeyboardButton("Сохранить_конигурацию")
                botton_reset_up = types.KeyboardButton("Импортировать_конигурацию")
                back = types.KeyboardButton("Назад")
                markup.add(botton22, botton_reset, botton_reset_up, back)
                bot.send_message(message.chat.id, text="Выполни запрос", reply_markup=markup)
        elif message.text == "Удалить_конфиг":
            bot.send_message(message.chat.id, "Введите последний октет ip, который нужно удалить.", reply_markup=types.ReplyKeyboardRemove())
            config_file_path_txt = f"cofigs.txt"
            with open(config_file_path_txt, 'rb') as file:
                config_content = file.read()
            bot.send_message(message.chat.id, config_content)
            bot.send_message(message.chat.id, "Введите последний октет ip, который нужно удалить. Например если нужно удалить ip адресс 10.10.0.47, то введите 47")
            bot.register_next_step_handler(message, del_vpn)
        elif message.text == "Добавить_конфиг":
            bot.send_message(message.chat.id, "Введите название нового конфига", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, add_vpn)
        elif message.text == "Конфиги":
            bot.send_message(message.chat.id, "Вот ваша конфигурация Wireguard")
            config_file_path = f"/etc/wireguard/wg0.conf"
            with open(config_file_path, 'rb') as file:
                bot.send_document(message.chat.id, file)
            with open(config_file_path, 'r') as file:
                config_content = file.read()
            bot.send_message(message.chat.id, config_content)
            file_list = glob.glob('/etc/wireguard/*.conf')
            for file_path in file_list:
                if os.path.basename(file_path) != 'wg0.conf':
                    with open(file_path, 'rb') as file:
                        bot.send_document(message.chat.id, document=file)
            config_file_path_txt = f"cofigs.txt"
            with open(config_file_path_txt, 'rb') as file:
                config_content = file.read()
            bot.send_message(message.chat.id, config_content)
#            bot.send_message(message.chat.id, "Конфигурационный файл успешно отправлен.")
        elif message.text == "Сохранить_конигурацию":
            subprocess.run(['scripts/backup.sh'])
            print("ok")
            bot.send_message(message.chat.id, text="Резервная копия создана")
        elif message.text == "Импортировать_конигурацию":
            subprocess.run(['scripts/restore.sh'])
            print("ok2")
            bot.send_message(message.chat.id, text="Резервная копия импортированна")
        elif message.text == "Установка_Wireguard":
            # Проверка наличия файла
            file_path = '/etc/wireguard/wg0.conf'
            if os.path.isfile(file_path):
                print(f"Файл {file_path} существует.")
#                bot.send_message(message.chat.id, "Wireguard уже настроен. \nХотите настроить заново?")
#                bot.send_message(message.chat.id, "Хотите установить все заново?")
#                bot.send_message(message.chat.id, text="Привет хозяин")
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                botton_yes = types.KeyboardButton("Да")
                botton_no = types.KeyboardButton("Нет")
                markup.add(botton_yes, botton_no)
                bot.send_message(message.chat.id, text="Wireguard уже настроен. \nХотите настроить заново?", reply_markup=markup)
            else:
                print(f"Файла {file_path} не существует.")
                bot.send_message(message.chat.id, "Запускаю установку Wireguard. \nПожалуйста дождитесь завершения установки.")
                subprocess.run(['scripts/start_wg.sh'])
                bot.send_message(message.chat.id, "Установка Wireguard завершена")
        elif (message.text == "Да"):
            bot.send_message(message.chat.id, "Удаляю конфиги!")
            command = "rm variables.sh && rm -r /etc/wireguard/ && mkdir /etc/wireguard/ && rm cofigs.txt"
            subprocess.run(command, shell=True)
#            # Удаление файла variables.sh
#            subprocess.run("rm variables.sh", shell=True)
#            # Удаление каталога /etc/wireguard/
#            subprocess.run("rm -r /etc/wireguard/", shell=True)
#            # Пауза для обеспечения времени на завершение предыдущей команды
#            time.sleep(10)
#            # Создание каталога /etc/wireguard/
#            subprocess.run("mkdir /etc/wireguard/", shell=True)
#            # Удаление файла cofigs.txt
#            subproces.run("rm cofigs.txt", shell=True)
            bot.send_message(message.chat.id, "Запускаю установку Wireguard")
            subprocess.run(['scripts/start_wg.sh'])
            bot.send_message(message.chat.id, "Установка Wireguard завершена")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Мониторинг")
            button2 = types.KeyboardButton("Администрирование")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, text="Назад", reply_markup=markup)
        elif (message.text == "Нет"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Мониторинг")
            button2 = types.KeyboardButton("Администрирование")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, text="Назад", reply_markup=markup)
        elif (message.text == "Назад"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Мониторинг")
            button2 = types.KeyboardButton("Администрирование")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, text="Назад", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")
        message_text = message.text
        print(message_text)
    elif(str(message.chat.id) != mainid):
        bot.send_message(message.chat.id, text="Привет, {0.first_name}! Ты заплутал!!".format(message.from_user))

bot.polling(none_stop=True)

