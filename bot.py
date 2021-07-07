import config
import functions
import database
import telebot
import json

from telebot import types

print("Бот запущен. Нажмите Ctrl+C для завершения")

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['location'])
def handle_loc(message):
    point = str(message.location.longitude) + '%2C'+ str(message.location.latitude)
    bot.send_message(message.chat.id, text=functions.search_map(point))

@bot.message_handler(commands=["start"])
def cmd_start(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
	button1 = types.KeyboardButton(text='\U0001F680') #ГУАП
	button2 = types.KeyboardButton(text='\U0001F4B5') #Стипендии и мат.помощь
	button3 = types.KeyboardButton(text='\U0001F1F7\U0001F1FA') #военка 
	button4 = types.KeyboardButton(text='\U0001F32F') #еда
	button5 = types.KeyboardButton(text='\U00002753') #помощь
	keyboard.add(button1, button2, button3, button4, button5)
	bot.send_message(message.chat.id, text=database.posts["start"], reply_markup=keyboard, parse_mode="MarkdownV2")

@bot.message_handler(content_types=['text'])
def f1(message):
    try:
        num = float(message.text)
        functions.dec(bot, num, message.chat.id, message.message_id, 1)
    except:
        functions.text(bot, message)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    keyboard = types.InlineKeyboardMarkup()

    # переход от ГУАП

    if call.data == "decanats": 
        key_1 = types.InlineKeyboardButton(text='ФПТИ', callback_data='fpti')
        key_2 = types.InlineKeyboardButton(text='ВУЦ', callback_data='vuc')
        keyboard.add(key_1, key_2)
        key_3 = types.InlineKeyboardButton(text='ИНДО', callback_data='indo')
        key_4 = types.InlineKeyboardButton(text='ФДПО', callback_data='fdpo')
        key_5 = types.InlineKeyboardButton(text='ФСПО', callback_data='fspo')
        keyboard.add(key_3, key_4, key_5)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=database.posts[call.data], reply_markup=keyboard, parse_mode="MarkdownV2")

    elif call.data == "buildings":
        key_1 = types.InlineKeyboardButton(text='БМ', callback_data='bm')
        key_2 = types.InlineKeyboardButton(text='Гаста', callback_data='gasta')
        keyboard.add(key_1, key_2)
        key_3 = types.InlineKeyboardButton(text='Ленса', callback_data='lensa')
        key_4 = types.InlineKeyboardButton(text='Колледж', callback_data='kol')
        keyboard.add(key_3, key_4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=database.posts[call.data], reply_markup=keyboard, parse_mode="MarkdownV2")

    elif call.data == "dorms":
        key_1 = types.InlineKeyboardButton(text='Жукова', callback_data='dorm1')
        key_2 = types.InlineKeyboardButton(text='Передовиков', callback_data='dorm2')
        keyboard.add(key_1, key_2)
        key_3 = types.InlineKeyboardButton(text='Варшавская', callback_data='dorm3')
        key_4 = types.InlineKeyboardButton(text='МСГ', callback_data='msg')
        keyboard.add(key_3, key_4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=database.posts[call.data], reply_markup=keyboard, parse_mode="MarkdownV2")

    elif call.data == "society":
        key_1 = types.InlineKeyboardButton(text='Профсоюз', callback_data='prof')
        key_2 = types.InlineKeyboardButton(text='ССО', callback_data='sso')
        keyboard.add(key_1, key_2)
        key_3 = types.InlineKeyboardButton(text='Отряды', callback_data='otryad')
        key_4 = types.InlineKeyboardButton(text='Объединения', callback_data='assoc')
        keyboard.add(key_3, key_4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=database.posts[call.data], reply_markup=keyboard, parse_mode="MarkdownV2")

    # переход от стипендии и мп

    elif call.data == "stipendium":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=database.stependiya, parse_mode="MarkdownV2")

    elif call.data == "financial_assistance":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=database.mp, parse_mode="MarkdownV2")

    # переход от деканатов

    elif (call.data == "fpti" or call.data == "vuc" or call.data == "indo" or call.data == "fdpo" or call.data == "fspo"):
        functions.dec(bot, call.data, call.message.chat.id, call.message.message_id, 2)

    # переход от корпусов

    elif (call.data == "bm" or call.data == "gasta" or call.data == "lensa" or call.data == "kol"):
        file = open(database.corps[call.data]["photo"], 'rb')
        text1 = database.corps[call.data]["adress"] + "\n\n" + database.corps[call.data]["way"]
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(chat_id=call.message.chat.id, photo=file, caption=text1)
        bot.send_location(call.message.chat.id, database.corps[call.data]["latitude"], database.corps[call.data]["longitude"]) 

    # переход от общежитий

    elif (call.data == "dorm1" or call.data == "dorm2" or call.data == "dorm3" or call.data == "msg"):
        text1 = database.dorms[call.data]["adress"] + "\n\n" + database.dorms[call.data]["fio"] + "\nтел.: " + database.dorms[call.data]["telefon"] 
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)
        bot.send_location(call.message.chat.id, database.dorms[call.data]["latitude"], database.dorms[call.data]["longitude"]) 

    # переход от объединений

    elif call.data == "prof":
        text1 = "Профсоюз\n\nГруппа профкома Вконтакте:\nvk: " + database.organization["prof"]["vk_prof"] + "\n\nВ этой группе ты можешь найти профсоюзы каждого института, просто посмотри ссылки группы"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)
        for i in database.organization["prof"]["prec"]:
            if i["vk"] == "":
                text1 = i["fio"] + "\n\n" + i["telefon"] + "\n" + i["mail"] + "\n" + i["vk"]
            else:
                text1 = i["fio"] + "\n" + i["telefon"] + "\n" + i["mail"] + "\n" + i["vk"]
            bot.send_message(call.message.chat.id, text=text1)
    elif call.data == "sso":
        text1 = "ССО - СтудСовет\n\nvk: " + database.organization["sso"]["vk_sso"] + "\n\n" + database.organization["sso"]["fio"] + "\nvk: " + database.organization["sso"]["vk"]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)
    elif call.data == "otryad":
        text1 = "Отряды\n\nСсылка на группу обо всех студенческих отрядах:\nvk: " + database.organization["otryad"]["vk_otryad"]
        key_0 = types.InlineKeyboardButton(text=database.organization["otryad"]["groups"][0]["name"], callback_data='11')
        key_1 = types.InlineKeyboardButton(text=database.organization["otryad"]["groups"][1]["name"], callback_data='12')
        keyboard.row(key_0, key_1)
        key_2 = types.InlineKeyboardButton(text=database.organization["otryad"]["groups"][2]["name"], callback_data='13')
        key_3 = types.InlineKeyboardButton(text=database.organization["otryad"]["groups"][3]["name"], callback_data='14')
        keyboard.row(key_2, key_3)
        key_4 = types.InlineKeyboardButton(text=database.organization["otryad"]["groups"][4]["name"], callback_data='15')
        keyboard.row(key_4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1, reply_markup=keyboard)

    elif call.data == "assoc":
        key_0 = types.InlineKeyboardButton(text='Видеостудия', callback_data='0')
        key_1 = types.InlineKeyboardButton(text='Чирлидинг', callback_data='1')
        keyboard.row(key_0, key_1)
        key_2 = types.InlineKeyboardButton(text='КВН', callback_data='2')
        key_3 = types.InlineKeyboardButton(text='Крылья', callback_data='3')
        keyboard.row(key_2, key_3)
        key_4 = types.InlineKeyboardButton(text='МУЗГУАП', callback_data='4')
        key_5 = types.InlineKeyboardButton(text='Пресс-Центр', callback_data='5')
        keyboard.row(key_4, key_5)
        key_6 = types.InlineKeyboardButton(text='Радио', callback_data='6')
        key_7 = types.InlineKeyboardButton(text='SUAI SHOW', callback_data='7')
        keyboard.row(key_6, key_7)
        key_8 = types.InlineKeyboardButton(text='Танцы', callback_data='8')
        key_9 = types.InlineKeyboardButton(text='Фотостудия', callback_data='9')
        keyboard.row(key_8, key_9)
        key_10 = types.InlineKeyboardButton(text='Театр', callback_data='10')
        keyboard.row(key_10)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=database.posts["assoc"], reply_markup=keyboard, parse_mode="MarkdownV2")
       
    # переход от объединений

    elif (call.data == "0" or call.data == "1" or call.data == "2" or call.data == "3" or call.data == "4" or call.data == "5" or call.data == "6" or call.data == "7" or call.data == "8" or call.data == "9" or call.data == "10"):
        num = int(call.data)
        text1 = database.organization["assoc"][num]["name"] + "\n\n" + database.organization["assoc"][num]["descr"] + "\nvk: " + database.organization["assoc"][num]["vk"]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)

    # переход от отрядов

    elif (call.data == "11" or call.data == "12" or call.data == "13" or call.data == "14" or call.data == "15"):
        num = int(call.data) - 11
        text1 = database.organization["otryad"]["groups"][num]["name"] + ":\n\nvk: " + database.organization["otryad"]["groups"][num]["vk"]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text1)

bot.polling()
