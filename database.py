import mysql.connector
from mysql.connector import errorcode

def create_table():
    try:
        conn = mysql.connector.connect(
            user='root',
            password='P455W0RD',
            host='localhost',
            database='reparaciones'
        )
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            folio VARCHAR(7) NOT NULL,
            name_contacto VARCHAR(100) NOT NULL,
            contacto VARCHAR(20) NOT NULL,
            tipo_equipo VARCHAR(100) NOT NULL,
            marca VARCHAR(50) NOT NULL,
            modelo VARCHAR(100) NOT NULL,
            problema VARCHAR(50) NOT NULL,
            accesorios TEXT NOT NULL,
            observaciones TEXT,
            fecha_registro DATE NOT NULL,   
        )
        ''')

        conn.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con el nombre de usuario o la contraseña")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)
    else:
        conn.close()

def save_equipment(data):
    try:
        conn = mysql.connector.connect(
            user='root',
            password='P455W0RD',
            host='localhost',
            database='reparaciones'
        )
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO equipos (folio, name_contacto, contacto, tipo_equipo, marca, modelo, problema, accesorios, observaciones, fecha_registro)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', data)

        conn.commit()
    except mysql.connector.Error as err:
        print(err)
    else:
        conn.close()
