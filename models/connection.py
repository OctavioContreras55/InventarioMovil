import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'practica_db',
    }

def get_db_connection():    
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Conexion exitosa a la base de datos")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        conn.close()
        print("Conexion cerrada correctamente")
