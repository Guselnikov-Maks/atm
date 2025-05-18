import mysql.connector
import local_settings as settings
from datetime import datetime

def register_user(user_login, user_password, chat_id):
    try:
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
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'
        
def delete_user(chat_id):
    try:
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
        #select * from km where km.date >= date_format(now(), '%Y-%m-01') and km.date < date_format(now(), '%Y-%m-01') + interval 1 month;
        #select km from km where km.date >= date_format(now(), '%Y-%m-01') and km.date < date_format(now(), '%Y-%m-01') + interval 1 month;
        #select km from km where chat_id = %s and km.date >= date_format(now(), '%Y-%m-01') and km.date < date_format(now(), '%Y-%m-01') + interval 1 month
        cursor.execute("select km from km where chat_id = %s and km.date >= date_format(now(), '%Y-%m-01') and km.date < date_format(now(), '%Y-%m-01') + interval 1 month", (chat_id,))
        
        data = cursor.fetchall()
        kol = 0
        for i in data:
            kol += i[0]
            
        ret = 'Общее количетсво бензина залито в этом месяце: ' + str(kol)
        db.commit()
        db.close()
        return ret
    except mysql.connector.Error as err:
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
    print(result)
    
def add_zip(chat_id, name, number):

    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("insert into sklad (name, state, number, status, date, chat_id) value (%s, 'GOOD', %s, 'На руках', NOW(), %s)",
                       (name, number, chat_id))
        
        db.commit()
        db.close()
        return 'ZIP добавлен в базу данных в статусе GOOD'
    except mysql.connector.Error as err:
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'
    
def find_serial(chat_id, number):
    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM telegram.sklad where number = %s and chat_id = %s;",
                       (number, chat_id))
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except mysql.connector.Error as err:
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'
    
def spisat_zip(chat_id, number):
    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("update sklad set status = 'На складе' where chat_id = %s and number = %s",
                       (chat_id, number))
        data = cursor.fetchall()
        db.commit()
        db.close()
        return 'Статус изменен на <blockquote>На складе</blockquote>'
    except mysql.connector.Error as err:
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'
    
def change_status_zip(chat_id, number):
    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("update sklad set state = 'BAD' where chat_id = %s and number = %s",
                       (chat_id, number))
        data = cursor.fetchall()
        db.commit()
        db.close()
        return 'Статус изменен на <blockquote>BAD</blockquote>'
    except mysql.connector.Error as err:
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'
    
def good_list_zip(chat_id):
    try:
        db = mysql.connector.connect(user=settings.mysql_user,
                                 password=settings.mysql_password,
                                 host=settings.mysql_host,
                                 port=settings.mysql_port,
                                 database='telegram')
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM telegram.sklad where chat_id = %s and state = 'GOOD';",
                       (chat_id,))
        data = cursor.fetchall()
        db.commit()
        db.close()
        return data
    except mysql.connector.Error as err:
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'
    
def bad_list_zip(chat_id):
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
        db.close()
        return 'Произошла ошибка, обратитесь к администратору'