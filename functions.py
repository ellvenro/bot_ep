import telebot
import database
import config
import json
import requests

from telebot import types

# функция обрабатки чиселла и названия деканатов, примнимает бота, ключ для доступа к database.decanat, id сообщения и чата
def dec(bot, num, id, id_mes, i):
    text1 = database.decanat[num]["name"] + "\n\n" + database.decanat[num]["fio"] + "\nтел.: " + database.decanat[num]["telefon"] + "\nауд.: " + database.decanat[num]["aud"]
    if i == 1:
        bot.send_message(id, text=text1)
    else:
        bot.edit_message_text(chat_id=id, message_id=id_mes, text=text1)

# функция обработки текстовых сообщений, примнимает бота и сообщение
def text(bot, message):
    if message.text == '\U0001F680': #ГУАП
        keyboard = types.InlineKeyboardMarkup(row_width=5) 
        key_1 = types.InlineKeyboardButton(text='\U0001F468\U0000200D\U0001F393', callback_data='decanats')
        key_2 = types.InlineKeyboardButton(text='\U0001F4CD', callback_data='buildings')
        key_3 = types.InlineKeyboardButton(text='\U0001F3E0', callback_data='dorms')
        key_4 = types.InlineKeyboardButton(text='\U000026D3', callback_data='society')
        keyboard.add(key_1, key_2, key_3, key_4)
        bot.send_message(message.from_user.id, text=database.posts["guap"], reply_markup=keyboard, parse_mode="MarkdownV2")

    elif message.text == '\U0001F4B5': #Стипендии и мат.помощь
        keyboard1 = types.InlineKeyboardMarkup() 
        key_5 = types.InlineKeyboardButton(text='Стипендии', callback_data='stipendium')
        key_6 = types.InlineKeyboardButton(text='Мат. помощь', callback_data='financial_assistance')
        keyboard1.add(key_5, key_6)
        hello1 = 'Выберите то, что вам нужно'
        bot.send_message(message.from_user.id, text=hello1, reply_markup=keyboard1)

    elif message.text == '\U0001F1F7\U0001F1FA': #военка
        bot.send_message(message.chat.id, database.voenca, parse_mode="MarkdownV2")

    elif message.text == '\U0001F32F': #еда
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        button_back = types.KeyboardButton(text="Назад")
        keyboard.add(button_geo, button_back)
        bot.send_message(message.chat.id, text=database.posts["eat"], reply_markup=keyboard, parse_mode="MarkdownV2")
        bot.send_message(message.chat.id, "Скажи, где ты?", reply_markup=keyboard)

    elif message.text == '\U00002753': #помощь
        bot.send_message(message.chat.id, database.posts["help"], parse_mode="MarkdownV2")

    elif message.text == 'Назад':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
        button1 = types.KeyboardButton(text='\U0001F680') #ГУАП
        button2 = types.KeyboardButton(text='\U0001F4B5') #Стипендии и мат.помощь
        button3 = types.KeyboardButton(text='\U0001F1F7\U0001F1FA') #военка 
        button4 = types.KeyboardButton(text='\U0001F32F') #еда
        button5 = types.KeyboardButton(text='\U00002753') #помощь
        keyboard.add(button1, button2, button3, button4, button5)
        bot.send_message(message.chat.id, text="Главное меню", reply_markup=keyboard, parse_mode="MarkdownV2")

# функция поиска по БД 2гис, принимает строку (геоллокация), возвращает строку (список локаций и информации про них)
def search_map(point):
    key = config.API_key  # апи ключ
    q = 'где поесть' # текст поискового запроса
    radius = '1000' #радиус поиска
    duble_gis = 'https://catalog.api.2gis.com/3.0/items?q='+q+'&type=branch&fields=items.point,items.schedule&point='+point+'&radius='+radius+'&key='+key #поисковый запрос в 2гис

    r = requests.get(duble_gis)
    result = json.loads(r.text)

    result_str = ''
    for item in result["result"]["items"]:
        result_str += "Заведение: " + item['name'] +'\nАдресс: ' + item['address_name'] + '\n\n'  

    return result_str