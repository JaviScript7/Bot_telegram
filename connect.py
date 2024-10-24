import time
import mysql.connector
from mysql.connector import Error

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"  # Resetear el color

def conector():
    # Intentar conectar varias veces con un retraso
    for _ in range(7):  # Intentar 7 veces
        try:
            conn = mysql.connector.connect(
                user='root',
                password='P455W0RD',
                host='db_container_mysql',  # Nombre del servicio definido en Docker Compose
                database='reparaciones'
            )
            if conn.is_connected():
                print(f"{Colors.YELLOW}Conexión exitosa a MySQL{Colors.RESET}\n")
                break
        except Error as e:
            print(f"{Colors.RED}No se pudo conectar a MySQL: {e}{Colors.RESET}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar
    
    return conn
