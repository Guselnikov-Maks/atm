import mysql.connector
import local_settings as settings
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, filename="/var/log/bot/atm/db.log",filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

def register_user(user_login, user_password, chat_id):
    try:
        logging.info('Производится регистрация пользователя')
        db = mysql.connector.connect(user=settings.mysql_user,
                                    password=settings.mysql_password,
                                    host=settings.mysql_host,
                                    port=settings.mysql_port,
                                    database='telegram')
        
        cursor = db.cursor()
        cursor.execute("select chat_id from users where chat_id = %s", (chat_id,))
        result = cursor.fetchall()
        
        if result:
            db.close()
            return 'Вы уже есть в базе'
        else:
            cursor.execute("insert into users (chat_id, user_login, user_password) value (%s, %s, %s)",
                           (chat_id, user_login, user_password))
            db.commit()
            db.close()
            return 'Ваш логин успешно зарегистрирован в базе данных'
    except mysql.connector.Error as err:
        logging.error(err)
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'
        
def delete_user(chat_id):
    try:
        logging.info('Удаление пользователя')
        db = mysql.connector.connect(user=settings.mysql_user,
                                    password=settings.mysql_password,
                                    host=settings.mysql_host,
                                    port=settings.mysql_port,
                                    database='telegram')
        
        cursor = db.cursor()
        cursor.execute("select chat_id from users where chat_id = %s", (chat_id,))
        result = cursor.fetchall()
        if result:
            cursor.execute("delete from users where chat_id = %s", (chat_id,))
            db.commit()
            db.close()
            return 'Вы удаленны из базы'
        else:
            db.close()
            return 'Вас нет в базе'

    except mysql.connector.Error as err:
        logging.error(err)
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'

def get_user_data(chat_id):
    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("select user_login, user_password from users where chat_id = %s", (chat_id,))
        result = cursor.fetchall()
        
        if result:
            db.close()
            return result
        else:
            db.close()
            return 'Вас нет в базе'

    except mysql.connector.Error as err:
        logging.error(err)
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'

def add_gas(chat_id, gaz):
    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("insert into km (chat_id, km, date) value (%s, %s, NOW())",
                       (chat_id, gaz))
        
        db.commit()
        db.close()
        return 'Ваша заправка внесенна в базу'
    except mysql.connector.Error as err:
        logging.error(err)
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'
        
def get_km(chat_id):
    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("select km from km where chat_id = %s and km.date >= date_format(now(), '%Y-%m-01') and km.date < date_format(now(), '%Y-%m-01') + interval 1 month", (chat_id,))
        
        data = cursor.fetchall()
        kol = 0
        for i in data:
            kol += i[0]
            
        db.commit()
        db.close()
        return kol
    except mysql.connector.Error as err:
        logging.error(err)
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'


def get_gaz_list(chat_id):
    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("select km, date from km where chat_id = %s and km.date >= date_format(now(), '%Y-%m-01') and km.date < date_format(now(), '%Y-%m-01') + interval 1 month", (chat_id,))
        
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except mysql.connector.Error as err:
        logging.error(err)
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'


def get_user_gaz(chat_id):
    db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
    cursor = db.cursor()
    cursor.execute("select user_login, user_password from gaz where chat_id = %s", (chat_id,))
    result = cursor.fetchall()
    

    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM telegram.sklad where chat_id = %s and state = 'BAD';",
                       (chat_id,))
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except mysql.connector.Error as err:
        logging.error(err)
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'