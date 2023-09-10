

def create_db(conn):
    with conn.cursor() as cur:
        # cur.execute("""
        #             DROP TABLE phones;
        #             DROP TABLE client;
        #             """)
        # таблица с данными клиента
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS client(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(40) NOT NULL,
                    last_name VARCHAR(60) NOT NULL,
                    email VARCHAR(255) NOT NULL
                    );""")
        # таблица с номерами телефонов привязанная к таблице клиента по id
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS phones(
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE,
                    phone VARCHAR(12)
                    );""")
        
        conn.commit()  # фиксируем в БД

def name_id(conn, email):
    """Получает ID клиента по email т.к. похожых имен и фамилий много а телефона может не быть"""
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT id FROM client WHERE email = %s;
                    """, (email,))
        return cur.fetchone()[0]

def add_client(conn,first_name, last_name, email, phones=None):
    """Добавляет нового клиента"""   
    with conn.cursor() as cur:
        # добавляем клиента
        cur.execute("""
                    INSERT INTO client(first_name, last_name, email) VALUES (%s, %s , %s)
                    RETURNING id;
                    """, (first_name, last_name, email))
        client_id = cur.fetchone()[0]
        # добавляем телефон
        cur.execute("""
                    INSERT INTO phones(client_id, phone) VALUES (%s , %s);
                    """, (client_id, phones))        
        conn.commit()
        print('Клиент добавлен в базу!')

def add_phone(conn, client_id, phone):
    """Добавляет телефон к существующему клиенту"""  
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO phones(client_id, phone)  VALUES (%s , %s);
                    """, (client_id, phone))           
        conn.commit()
        print('Телефон добавлен в базу!')
        
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    """Изменяет данные существующего клиента"""
    with conn.cursor() as cur:       
        cur.execute("""
                    UPDATE client SET first_name=%s WHERE id=%s;""", (first_name, client_id))
        conn.commit()
        
        cur.execute("""
                    UPDATE client SET last_name=%s WHERE id=%s;""", (last_name, client_id))
        conn.commit()
        
        cur.execute("""
                    UPDATE client SET email=%s WHERE id=%s;""", (email, client_id))        
        conn.commit()
        
        cur.execute("""
                    UPDATE phones SET phone=%s  WHERE client_id=%s;
                    """, (phones, client_id))         
        conn.commit()
        print('Данные изменены!')

def delete_phone(conn, client_id, phone):
    """Удаляет телефон клиента"""
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM phones WHERE client_id=%s AND phone=%s;
                    """, (client_id, phone))         
        conn.commit()
        print('Телефон удален!')

def delete_client(conn, client_id):
    """Удаляет клиента"""
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM client WHERE id=%s;
                    """, (client_id,))
        conn.commit()
        
        print('Клиент удален!')
        
def find_client(conn):#, first_name=None, last_name=None, email=None, phone=None):
    
    with conn.cursor() as cur:
        # Можно написать запросы на каждый столбик, сделать поиск по одному вводу данных, таким способомне получилось.
        # cur.execute("""
        #             SELECT first_name, last_name, email, phone FROM client c
        #             LEFT JOIN phones p ON c.id = p.client_id
        #             WHERE first_name=%s;
        #             """, (name,))
        
        # объединяем таблицы с данными ителефонами для поиска клиентов
        cur.execute("""
                    SELECT first_name, last_name, email, phone FROM client c
                    LEFT JOIN phones p ON c.id = p.client_id;
                    """)
        return cur.fetchall()[0]        


