import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error
from connect import conector
from datetime import datetime
from analisis.analisis_datos import crear_grafico

def create_table():
    try:
        conn = conector()
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
            fecha_registro DATE NOT NULL   
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
        conn = conector()
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

# Consultar los datos del equipo por folio
def get_equipo_by_folio(folio):
    conn = conector()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM equipos WHERE folio = %s"
            cursor.execute(query, (folio,))
            result = cursor.fetchone()
            return result
        
        except Error as e:
            print(f"Error al consultar los datos del equipo: {e}")
            return None
        finally:
            cursor.close()
            conn.close()



def get_data_for_time(datos):
    conn = conector()
    val_dato = datos.strip()  # Eliminar espacios en blanco al inicio y al final
    
    if conn:
        try:
            datetime.strptime(val_dato, '%Y-%m-%d') # Verificar si el dato corresponde a un día (YYYY-MM-DD)
            cursor = conn.cursor()
            query = "SELECT tipo_equipo, COUNT(*) as cantidad FROM equipos WHERE fecha_registro = %s GROUP BY tipo_equipo;"
            cursor.execute(query, (val_dato,))
            result = cursor.fetchall()
            grafico = crear_grafico(result,dia="Dia")
            cursor.close()
            conn.close() 
            return grafico

        except Error as e:
            print(f"Error al consultar los datos: {e}")
            return None
        except ValueError:
            pass 

            

        # --------------------------------
        try:
            datetime.strptime(val_dato, '%Y-%m') # Verificar si el dato corresponde a un mes (YYYY-MM)
            cursor = conn.cursor()
            query = "SELECT tipo_equipo, COUNT(*) as cantidad FROM equipos WHERE DATE_FORMAT(fecha_registro,'%Y-%m') = %s  GROUP BY tipo_equipo;"
            cursor.execute(query, (val_dato,))
            result = cursor.fetchall()
            grafico = crear_grafico(result,dia="Mes")
            cursor.close()
            conn.close() 
            return grafico
        
        except Error as e:
            print(f"Error al consultar los datos: {e}")
            return None
        except ValueError:
            pass 
        finally:
            pass

        #---------------------------------
        try:
            start_date_str, end_date_str = val_dato.split()
            # Intentar parsear ambas fechas | Verificar si el dato corresponde a un rango de semana (YYYY-MM-DD YYYY-MM-DD)
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            
            if start_date <= end_date: # Verificar que el rango sea válido (fecha de inicio debe ser menor que fecha de fin)
                    cursor = conn.cursor()
                    query = "SELECT tipo_equipo, COUNT(*) as cantidad FROM equipos WHERE fecha_registro BETWEEN %s AND %s  GROUP BY tipo_equipo;"
                    cursor.execute(query, (start_date,end_date))
                    result = cursor.fetchall()
                    grafico = crear_grafico(result,dia="Semana")
                    cursor.close()
                    conn.close() 
                    return grafico
        
        except Error as e:
            print(f"Error al consultar los datos: {e}")
            return None
        except ValueError:
            pass 
        finally:
            pass

        return False  # Si no coincide con ninguno de los formatos
