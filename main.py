import local_settings as settings
import db as db
import web as web
import telebot
from telebot import types
import time
import os
import photo as phs


bot = telebot.TeleBot(settings.bot_token)
bot.delete_webhook()

bot.set_my_commands([
    telebot.types.BotCommand('/start', "Запустить бота и зарегистрироватся"),
    telebot.types.BotCommand('/add_gaz', 'Добавить заправку'),
    telebot.types.BotCommand('/get_gaz', 'Получить свои заправки'),
    telebot.types.BotCommand('/get_km', 'Получить пробег за месяц'),
    telebot.types.BotCommand('/get_gaz_list', 'Получить список заправок в этом месяце'),
    telebot.types.BotCommand('/register', 'Регистрация'),
    telebot.types.BotCommand('/help', 'Помощь'),
    telebot.types.BotCommand('/callback', 'обратная связь')
])

@bot.message_handler(commands=['start'])
def handle_start(message):
   msg = "Приветственное сообщение"
   chat_id = message.chat.id
   bot.send_message(message.chat.id, msg) 
   
   
@bot.message_handler(commands=['help'])
def handle_start(message):
   msg_1 = "Перед началом испотзованием бота вам необходимо пройти регистрацию сооответствующей командой или нажать на /register. Вам необходимо боту сообщить ваш логи и пароль от сайта, после бот проведет тестовую авторизацию"
   msg_2 = "После успешной авторизации можно использовать бота. Для правильного подсчета пробега необходимо указывать количество заправленного топлива в <b>литрах</b>"
   bot.send_message(message.chat.id, msg_1, parse_mode='html')
   bot.send_message(message.chat.id, msg_2, parse_mode='html')
   
@bot.message_handler(commands=['callback'])
def handle_start(message):
   msg = bot.send_message(message.chat.id, 'Введите одним сообщение текст который хотите сообщить администратору')
   bot.register_next_step_handler(msg, fcalbuck)
   
def fcalbuck(message):
    msg = "Полученно новое сообщение" 
    bot.send_message(7831441950, msg, parse_mode='html')
    bot.send_message(7831441950, message.text, parse_mode='html')
 
 
@bot.message_handler(commands=['get_km'])
def get_km(message):
    user = db.get_user_data(message.chat.id)
    bot.send_message(message.chat.id, 'Ожидайте')
    #Получил количество километров
    km = web.get_km(user[0][0], user[0][1])
    
    #Получаю заправки
    gaz = db.get_km(message.chat.id) * 10

    zapas = km - gaz
    
    if zapas > 0:
        msg = 'Ты красавчик, твой километраж больше чем количество заправленного бензина. Ты проехал <b>' + str(zapas) + 'км</b>, и у тебы в запасе ' + str(zapas / 10) + ' <b>литров</b>'
        msg_1 = 'В этом месяце ты проехал <b>' + str(km) + ' километров</b>, и заправился на <b>' + str(gaz / 10) + ' литров.</b>'
        bot.send_message(message.chat.id, msg_1, parse_mode='html')
        bot.send_message(message.chat.id, msg, parse_mode='html')
    if zapas < 0:
        msg = 'Твой километраж меньше чем заправленного бензина. Ты в минусе на <b>' + str(zapas) + 'km</b> или на <b>' + str(zapas / 10) + 'литров</b> бензина'
        msg_1 = 'В этом месяце ты проехал <b>' + str(km) + ' километров</b> и заправился на <b>' + str(gaz / 10) + ' литров</b>.'
        bot.send_message(message.chat.id, msg_1, parse_mode='html')
        bot.send_message(message.chat.id, msg, parse_mode='html')
    if zapas == 0:
        msg = 'Твой пробег равен количеству бензина'
        msg_1 = 'В этом месяце ты проехал ' + str(km) + ' километров, и заправился на ' + str(gaz / 10) + ' литров.'
        bot.send_message(message.chat.id, msg_1, parse_mode='html')
        bot.send_message(message.chat.id, msg, parse_mode='html')


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


bot.polling(none_stop=True, interval=0)
