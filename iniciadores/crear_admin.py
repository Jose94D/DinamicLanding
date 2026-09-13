import sqlite3
from werkzeug.security import generate_password_hash

conexion = sqlite3.connect('database.db')
cursor = conexion.cursor()

username = "admin"
password = "admin123" # Puedes cambiarla aquí
hash_password = generate_password_hash(password)

try:
    cursor.execute("INSERT INTO admin (username, password_hash) VALUES (?, ?)", (username, hash_password))
    conexion.commit()
    print(f"¡Usuario '{username}' creado exitosamente! Contraseña: {password}")
except sqlite3.IntegrityError:
    print("El usuario ya existe en la base de datos.")
finally:
    conexion.close()