import local_settings as settings
import db as db
import web as web
import telebot
from telebot import types
import time
import os


bot = telebot.TeleBot(settings.bot_token)
bot.delete_webhook()

bot.set_my_commands([
    telebot.types.BotCommand('/start', "Запустить бота и зарегистрироватся"),
    telebot.types.BotCommand('/add_gaz', 'Добавить заправку'),
    telebot.types.BotCommand('/get_gaz', 'Получить свои заправки'),
    telebot.types.BotCommand('/get_km', 'Получить пробег за месяц'),
    telebot.types.BotCommand('/get_gaz_list', 'Получить список заправок в этом месяце'),
    telebot.types.BotCommand('/register', 'Регистрация'),
    telebot.types.BotCommand('/test', 'Test'),
    telebot.types.BotCommand('/exel', 'Получить EXEL'),
    telebot.types.BotCommand('/delete', 'Удалить меня'),
    telebot.types.BotCommand('/sklad', 'Работа со складом')
])

@bot.message_handler(commands=['start'])
def handle_start(message):
   msg = "Приветственное сообщение"
   chat_id = message.chat.id
   bot.send_message(message.chat.id, msg) 
   
@bot.message_handler(commands=['get_km'])
def get_km(message):
    user = db.get_user_data(message.chat.id)
    bot.send_message(message.chat.id, 'Ожидайте')
    bot.send_message(message.chat.id, web.get_km(user[0][0], user[0][1]))


@bot.message_handler(commands=['add_gaz'])
def fadd_gaz(message):
    msg = bot.send_message(message.chat.id, 'Отправте количество литров которое вы заправили')
    bot.register_next_step_handler(msg, add_gaz)
    
def add_gaz(message):
    try:
        numb = int(message.text)
        msg = db.add_gas(message.chat.id, numb)
        bot.send_message(message.chat.id, msg)
    except:
        bot.send_message(message.chat.id, 'Не удалось добавить')
    
    
@bot.message_handler(commands=['get_gaz'])
def get_gaz(message):
    msg = db.get_km(message.chat.id)
    bot.send_message(message.chat.id, msg)
    
@bot.message_handler(commands=['get_gaz_list'])
def get_gaz(message):
    data = db.get_gaz_list(message.chat.id)
    str_test =''
    for i in range(0, len(data)):
        msg = str(data[i][1]) + ' вы заправились на ' + str(data[i][0]) + ' литров'
        str_test += ('<i>' + str(data[i][1])) + '</i>' + '\n<span class="tg-spoiler">Вы заправились на ' + str(data[i][0]) + ' литров</span>\n'
        time.sleep(0.5)
        
    bot.send_message(message.chat.id, str_test, parse_mode='html')

 
 
@bot.message_handler(commands=['exel'])
def exel(message):
    bot.send_message(message.chat.id, 'Ожидайте, идет подготовка файла')
    user = db.get_user_data(message.chat.id)
    file = web.get_list(user[0][0], user[0][1], message.chat.id)
    doc = open(file, 'rb')
    bot.send_document(message.chat.id, doc)
    bot.send_message(message.chat.id, 'Вам был отправлен файл.')
    os.remove(file)
    bot.send_message(message.chat.id, 'Файл с сервера был удален')

@bot.message_handler(commands=['test'])
def test(message):
    str_b = '<b>Это b </b>'
    str_i = '<i> This is i </i>'
    str_u = '<u>This is u</u>'
    str_s = '<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>'
    str_span = '<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>'
    str_bold = '<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>'
    str_a = '<a href="http://www.example.com/">inline URL</a>'
    str_line = '<a href="tg://user?id=7831441950">inline mention of a user my</a>'
    str_em = '<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>'
    str_code = '<code>inline fixed-width code</code>'
    str_pre = '<pre>pre-formatted fixed-width code block</pre>'
    str_pre_code = '<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>'
    str_block = '<blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>'
    str_q = '<blockquote expandable>Expandable block quotation started\nExpandable block quotation continued\nExpandable block quotation continued\nHidden by default part of the block quotation started\nExpandable block quotation continued\nThe last line of the block quotation</blockquote>'
    bot.send_message(message.chat.id, str_b, parse_mode='html')
    bot.send_message(message.chat.id, str_i, parse_mode='html')
    bot.send_message(message.chat.id, str_u, parse_mode='html')
    bot.send_message(message.chat.id, str_s, parse_mode='html')
    bot.send_message(message.chat.id, str_span, parse_mode='html')
    bot.send_message(message.chat.id, str_bold, parse_mode='html')
    bot.send_message(message.chat.id, str_line, parse_mode='html')
    bot.send_message(message.chat.id, str_em, parse_mode='html')
    bot.send_message(message.chat.id, str_code, parse_mode='html')
    bot.send_message(message.chat.id, str_pre, parse_mode='html')
    bot.send_message(message.chat.id, str_pre_code, parse_mode='html')
    bot.send_message(message.chat.id, str_block, parse_mode='html')
    bot.send_message(message.chat.id, str_q, parse_mode='html')
    bot.send_message(message.chat.id, str_a, parse_mode='html')
    bot.send_message(message.chat.id, 'Message')

    
    
@bot.message_handler(commands=['delete'])
def delete_user(message):
    bot.send_message(message.chat.id, db.delete_user(message.chat.id))

@bot.message_handler(commands=['register'])
def registration(message):
    msg = bot.send_message(message.chat.id, "Введите ваш логин")
    bot.register_next_step_handler(msg, enter_password)
    
def enter_password(message):
    msg = bot.send_message(message.chat.id, "Введите ваш пароль")
    bot.register_next_step_handler(msg, register_user, message.text)
    
def register_user(message, login):
    ret = 'Ваш логин: ' + login + '\nВаш пароль: ' + message.text
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_tru')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='no_true')
    markup.row(btn_yes, btn_no)
    bot.send_message(message.chat.id, ret, parse_mode='Markdown', reply_markup=markup)
    


@bot.message_handler(commands=['sklad'])
def sklad(message):
    markup = types.InlineKeyboardMarkup()
    btn_add = types.InlineKeyboardButton(text='Добавить запись', callback_data='add_zip')
    btn_del = types.InlineKeyboardButton(text='Удалить запись', callback_data='del_zip')
    btn_update = types.InlineKeyboardButton(text='Изменить статус', callback_data='change_zip')
    btn_list = types.InlineKeyboardButton(text='GOOD список', callback_data='get_good')
    btn_bad = types.InlineKeyboardButton(text='BAD список', callback_data='get_dab')
    btn_sps = types.InlineKeyboardButton(text='Списать', callback_data='spisat_zip')
    btn_all = types.InlineKeyboardButton(text='Получить весь список склада EXEL', callback_data='get_all')
    msg = 'Что вы хотите сделать?'
    markup.row(btn_add, btn_update)
    markup.row(btn_list, btn_bad)
    markup.row(btn_sps)
    markup.row(btn_all)
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=markup)
    


def add_zip(message):
    ms = bot.send_message(message.chat.id, 'Введи серийный номер')
    bot.register_next_step_handler(ms, add_zip_serial, message.text)
    
def add_zip_serial(message, name):
    msg = 'Проверте правильность ввода Наименования ЗИП: <blockquote>' + name + '</blockquote> Серийный номер: <blockquote>' + message.text + '</blockquote>'
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_zip_add')
    btn_no = types.InlineKeyboardButton(text='Нет', callback_data='no_true')
    markup.row(btn_yes, btn_no)
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=markup)
    
def spis_zip(message):
    first_msg = 'Идет поиск по серийному номеру: <blockquote>' + message.text + '</blockquote>'
    bot.send_message(message.chat.id, first_msg, parse_mode='html')
    data = db.find_serial(message.chat.id, message.text)

    if len(data) > 1:
        bot.send_message(message.chat.id, 'Найдено большо одной позиции, обратитесь к администратору')
    elif len(data) == 0:
        bot.send_message(message.chat.id, 'С таким серийным номером нет позиций')
    else:
        msg_zip = 'Наименование: <blockquote>' + data[0][1] + '</blockquote> Серийный номер: <blockquote>' + data[0][3] + '</blockquote> Статус: <blockquote>' + data[0][2] + '</blockquote>'
        markup = types.InlineKeyboardMarkup()
        btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_spisat')
        btn_no = types.InlineKeyboardButton('Нет', callback_data='no_true')
        markup.row(btn_yes, btn_no)
        bot.send_message(message.chat.id, msg_zip, parse_mode='html', reply_markup=markup)

def change_status_zip(message):
    first_msg = 'Идет поиск по серийному номеру: <blockquote>' + message.text + '</blockquote>'
    bot.send_message(message.chat.id, first_msg, parse_mode='html')
    data = db.find_serial(message.chat.id, message.text)

    if len(data) > 1:
        bot.send_message(message.chat.id, 'Найдено большо одной позиции, обратитесь к администратору')
    elif len(data) == 0:
        bot.send_message(message.chat.id, 'С таким серийным номером нет позиций')
    else:
        msg_zip = 'Наименование: <blockquote>' + data[0][1] + '</blockquote> Серийный номер: <blockquote>' + data[0][3] + '</blockquote> Статус: <blockquote>' + data[0][2] + '</blockquote>'
        markup = types.InlineKeyboardMarkup()
        btn_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_change_status_zip')
        btn_no = types.InlineKeyboardButton('Нет', callback_data='no_true')
        markup.row(btn_yes, btn_no)
        bot.send_message(message.chat.id, msg_zip, parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def response(function_call):
    if function_call.message:           
        if function_call.data == "yes_tru":
            str = function_call.message.text.split()
            user_login = str[2]
            user_password = str[5]
            bot.send_message(function_call.message.chat.id, db.register_user(user_login, user_password, function_call.message.chat.id))
            bot.send_message(function_call.message.chat.id, 'Ожидайте, идет авторизация')
            
            user = db.get_user_data(function_call.message.chat.id)
            bot.send_message(function_call.message.chat.id, web.test_auth(user[0][0], user[0][1]))

            
        if function_call.data == 'yes_register':
            print('Начать регитстрацию')
        if function_call.data == "no_true":
            bot.send_message(function_call.message.chat.id, 'начните сначала')
        if function_call.data == 'add_zip':
            msg_add = bot.send_message(function_call.message.chat.id, 'Ведите наименование ЗИП')
            bot.register_next_step_handler(msg_add, add_zip)
            
        if function_call.data == 'change_zip':
            msg = bot.send_message(function_call.message.chat.id, 'Введите серийный номер')
            bot.register_next_step_handler(msg, change_status_zip)
        if function_call.data == 'del_zip':
            bot.send_message(function_call.message.chat.id, 'Удплить')
        if function_call.data == 'get_good':
            data = db.good_list_zip(function_call.message.chat.id)
            for i in range(0, len(data)):
                test_str = 'Наименование: <blockquote>' + data[i][1] + '</blockquote>Серийный номер: <blockquote>' + data[i][3] + '</blockquote>'
                bot.send_message(function_call.message.chat.id, test_str, parse_mode='html')
                time.sleep(0.5)
            
            
        if function_call.data == 'get_dab':
            data = db.bad_list_zip(function_call.message.chat.id)
            for i in range(0, len(data)):
                test_str = 'Наименование: <blockquote>' + data[i][1] + '</blockquote>Серийный номер: <blockquote>' + data[i][3] + '</blockquote>'
                bot.send_message(function_call.message.chat.id, test_str, parse_mode='html')
                time.sleep(0.5)
            
            
            
            
            
        if function_call.data == 'get_all':
            bot.send_message(function_call.message.chat.id, 'Получить весь список склада')
        if function_call.data == 'yes_zip_add':
            str = function_call.message.text.split()
            num = 0
            num_serial = 0
            i = 0
            while i < len(str):
                if str[i] == 'Серийный':
                    num = i
                if str[i] == 'номер:':
                    num_serial = i + 1
                i += 1
            tmp_str = ''
            for i in range(5, num):
                tmp_str += str[i] + ' '

            number_zip = str[num_serial]
            otvet = db.add_zip(function_call.message.chat.id, tmp_str, number_zip)
            bot.send_message(function_call.message.chat.id, otvet)
        if function_call.data == 'spisat_zip':
            msg = bot.send_message(function_call.message.chat.id, 'Введити серийный номер списываемого ЗИП:')
            bot.register_next_step_handler(msg, spis_zip)
        if function_call.data == 'yes_spisat':
            str = function_call.message.text.split()
            num = 0
            i = 0
            while i < len(str):
                if str[i] == 'номер:':
                    num = i + 1
                i += 1
            otc = db.spisat_zip(function_call.message.chat.id, str[num])
            bot.send_message(function_call.message.chat.id, otc, parse_mode='html')
        if function_call.data == 'yes_change_status_zip':
            str = function_call.message.text.split()
            i = 0
            num_serial = 0
            while i < len(str):
                if str[i] == 'номер:':
                    num_serial = i + 1
                i += 1
            otvet = db.change_status_zip(function_call.message.chat.id, str[num_serial])
            bot.send_message(function_call.message.chat.id, otvet, parse_mode='html')

bot.polling(none_stop=True, interval=0)
