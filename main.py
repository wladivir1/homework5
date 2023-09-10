import psycopg2
from config import host, user, password, db_name
from db_main import *


def name_input():
    name = ''
    while not name:
        name = input('Введите имя: ').capitalize()
    return name

def surname_input():
    surname = ''
    while not surname:
        surname = input('Введите фамилию: ').capitalize()
    return surname

def email_input():
    mail = ''
    while not mail:
        mail = input('Введите mail: ')
    return mail

def connect(host, user, password, db_name):
    # подключаемся к СУБД
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        
        create_db(conn)
        print('----Управление базой клиентов----')
        print()
        print('''1-Добавить нового клиента
              \n2-Добавить номер телефона
              \n3-Изменить данные о клиенте
              \n4-Удалить номер телефона 
              \n5-Удалить клиента
              \n6-Поиск клиента по: имени, фамилии, email, телефону
              \n7-Закрыть программу ''')
        
        control_bd = ''
        while control_bd != 7:
            print()
            control_bd = int(input('Введите цифру из списка: '))
            # добавляем клиента
            if control_bd == 1:
                name = name_input()
                surname = surname_input()
                mail = email_input() 
                number = input('Введите номер телефона: ')                       
                add_client(conn, name, surname, mail, number)
            # добавляем номер телефона    
            elif control_bd == 2:
                mail = email_input()
                number = input('Введитеномер телефона: ')                
                client_id = name_id(conn, mail)           
                add_phone(conn, client_id, number)
            # изменяем данные    
            elif control_bd == 3:
                mail = email_input()
                name = name_input()
                surname = surname_input()
                change_mail = email_input()
                change_number = input('Введите новый номер: ')               
                client_id = name_id(conn, mail)
                change_client(conn, client_id, name, surname, change_mail, change_number)
            # удаляем телефон    
            elif control_bd == 4:
                mail = email_input()
                delete_number = input('Введите номер для удаления: ')               
                client_id = name_id(conn, mail)
                delete_phone(conn, client_id, delete_number)
            # удаляем клиента    
            elif control_bd == 5:
                mail = email_input()               
                client_id = name_id(conn, mail)
                delete_client(conn, client_id)
            # поис клиента по БД   
            elif control_bd == 6:
                client = input('Введите имя, фамилию, email или номер телефона: ')
                clientbd = find_client(conn)
            
                if client in clientbd:
                    print(f'{clientbd[0]} {clientbd[1]} {clientbd[2]} {clientbd[3]}') 
                else:
                    print('Клиента нет в базе данных!') 
            elif control_bd == 7:
                continue;                                         
            else:
                print('Вы ввели не правельное значение.')
    # обрабатываем и выводим ошибки                           
    except Exception as _ex:
        print('[INFO] Error while working with PostgresSQL', _ex)
    # закрываем соединение с БД    
    finally:
        if conn:
            conn.close()
            print('[INFO] PostgreSQL connection close')

if __name__ == '__main__':
    connect(host, user, password, db_name)            