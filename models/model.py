from .connection import get_db_connection
import hashlib, re

def add_user(username, email, password):
    conn = get_db_connection()
    if not conn:
        return False, "Error de conexión a la base de datos."
    if len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres."
    if not re.match("^[a-zA-Z0-9]+$", username):
        return False, "El nombre de usuario solo puede contener letras y números."
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        return False, "El correo electrónico no es válido."
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
    if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password):
        return False, "La contraseña debe contener al menos una letra mayúscula, una minúscula y un número."
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "El correo electrónico ya está registrado."
        cursor.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "El nombre de usuario ya existe."
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("INSERT INTO usuarios (username, email, password) VALUES (%s, %s, %s)", (username, email, password_hash))
        conn.commit()
        return True, "Usuario registrado exitosamente."
    except Exception as e:
        return False, f"Error al registrar usuario: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def authenticate_user(username, password):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        
        # Hashear el password para ser mas seguro
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (username, password_hash))
        user = cursor.fetchone()
        if user:
            return{
                "id": user[0],
                "username": user[1],
                "email": user[2]
            }
        return None
    except Exception as e:
        print(f"Error al autenticar usuario: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
