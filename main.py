import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup
import requests
import time
import json
from bs4 import BeautifulSoup
import pandas

token = '6297240827:AAFkw8mg5m_ZoxI2JThokSq-wFX-vq77_jk'
bot = telebot.TeleBot(token)
flag1 = 0

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("Найти проект")
    btn2 = types.KeyboardButton("Найти вакансию")
    btn3 = types.KeyboardButton("Посмотреть заявки (для руководителей)")
    btn4 = types.KeyboardButton("Подписаться на систему уведомлений о новых заявках (для руководителей)")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text="Здравствуйте, {0.first_name}, выберите одну из доступных команд.".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global flag1
    if (message.text == "Найти проект"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Ввести ключевое слово для поиска проекта")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, back)
        bot.send_message(message.chat.id, text="Подтвердите действие", reply_markup=markup)

    elif (message.text == "Найти вакансию"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Ввести ключевое слово для поиска вакансии")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, back)
        bot.send_message(message.chat.id, text="Подтвердите действие", reply_markup=markup)

    elif (message.text == "Посмотреть заявки (для руководителей)"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Ввести id проекта для просмотра заявок")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, back)
        bot.send_message(message.chat.id, text="Подтвердите действие", reply_markup=markup)

    elif (message.text == "Подписаться на систему уведомлений о новых заявках (для руководителей)"):
        if flag1 == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton("Ввести id проекта для подписки на систему уведомлений о новых заявках")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, back)
            bot.send_message(message.chat.id, text="Подтвердите действие", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton("Отключить")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, back)
            bot.send_message(message.chat.id, text="Система уведомлений сейчас активна.", reply_markup=markup)

    elif (message.text == "Вернуться в главное меню"):
        markup: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Найти проект")
        button2 = types.KeyboardButton("Найти вакансию")
        button3 = types.KeyboardButton("Посмотреть заявки (для руководителей)")
        button4 = types.KeyboardButton("Подписаться на систему уведомлений о новых заявках (для руководителей)")
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    elif (message.text == "Ввести id проекта для просмотра заявок"):
        msg = bot.send_message(message.chat.id, 'Введите id проекта:')
        def parse(message):
            url = requests.get(f'https://cabinet.miem.hse.ru/public-api/students/project/application/{message.text}')
            flag = 0
            if url.status_code == 200:
                bot.send_message(message.chat.id, text="Заявки на проект:")
                information = url.json()
                k = 1
                for person in information["data"]:
                    bot.send_message(message.chat.id,
                                 text="Заявка №" + str(k) + ".\n" + "ФИО: " + person["name"] + "\n" +
                                 "Группа: " + person["group"] + "\n" + "Вакансия: " +
                                 person["role"] + "\n" + "Почта: " + person["email"][0])
                    k = k + 1
                    flag = 1
                if flag == 0:
                    bot.send_message(message.chat.id, text="По заданному id проекта заявок не найдено.")
            else:
                bot.send_message(message.chat.id, text="Не найдено проекта по заданному id.")
        bot.register_next_step_handler(msg, parse)

    elif (message.text == "Ввести ключевое слово для поиска проекта"):
        msg = bot.send_message(message.chat.id, 'Введите ключевое слово:')
        def parse(message):
            bot.send_message(message.chat.id, text=f"Наименования проектов, отобранные по ключевому слову '{message.text}':")
            url = requests.get('https://cabinet.miem.hse.ru/public-api/vacancy/list')
            information = url.json()
            flag = 0
            k = 1
            for vacancy in information["data"]:
                if str(message.text).lower() in vacancy["project_name_rus"].lower():
                    flag = 1
                    bot.send_message(message.chat.id,
                                     text="№" + str(k) + ".\n" + "Проект: " + vacancy["project_name_rus"])
                    k = k + 1
            if flag == 0:
                bot.send_message(message.chat.id, text="По заданному ключевому слову проектов не найдено.")
        bot.register_next_step_handler(msg, parse)

    elif (message.text == "Ввести ключевое слово для поиска вакансии"):
        msg = bot.send_message(message.chat.id, 'Введите ключевое слово')
        def parse(message):
            bot.send_message(message.chat.id, text=f"Наименования вакансий, отобранные по ключевому слову '{message.text}':")
            url = requests.get('https://cabinet.miem.hse.ru/public-api/vacancy/list')
            information = url.json()
            flag = 0
            k = 1
            for vacancy in information["data"]:
                if str(message.text).lower() in vacancy["vacancy_role"].lower():
                    flag = 1
                    bot.send_message(message.chat.id,
                                     text= "№" + str(k) + ".\n" + "Вакансия: " + vacancy["vacancy_role"] + "\n" + "Проект: " +
                                           vacancy["project_name_rus"])
                    k = k + 1
            if flag == 0:
                bot.send_message(message.chat.id, text = "По заданному ключевому слову вакансий не найдено.")
        bot.register_next_step_handler(msg, parse)

    elif (message.text == "Ввести id проекта для подписки на систему уведомлений о новых заявках"):
        msg = bot.send_message(message.chat.id, 'Введите id проекта:')
        def parse(message):
            global flag1
            url = requests.get(f'https://cabinet.miem.hse.ru/public-api/students/project/application/{message.text}')
            if url.status_code == 200:
                information = url.json()
                flag1 = 1
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                btn1 = types.KeyboardButton("Отключить")
                back = types.KeyboardButton("Вернуться в главное меню")
                markup.add(btn1, back)
                bot.send_message(message.chat.id, text="Подключена новая система уведомлений.", reply_markup=markup)
                k_new = 0
                while(flag1 == 1):
                    a = []
                    k_prev = k_new
                    k_new = 0
                    for person in information["data"]:
                        k_new = k_new + 1
                        a.append([person["name"], person["group"], person["role"], person["email"][0]])
                    time.sleep(10)
                    if (k_new > k_prev and k_prev != 0):
                        for i in range(k_prev, k_new):
                            bot.send_message(message.chat.id,
                                             text="Заявка №" + str(i + 1) + ".\n" + "ФИО: " + a[i][0] + "\n" +
                                                  "Группа: " + a[i][1] + "\n" + "Вакансия: " +
                                                  a[i][2] + "\n" + "Почта: " + a[i][3])
            else:
                bot.send_message(message.chat.id, text="Не найдено проекта по заданному id.")
        bot.register_next_step_handler(msg, parse)

    elif (message.text == "Отключить"):
        flag1 = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Ввести id проекта для подписки на систему уведомлений о новых заявках")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, back)
        bot.send_message(message.chat.id, text="Система уведомлений отключена.", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="Невозможно обработать команду")

bot.polling(none_stop=True)
