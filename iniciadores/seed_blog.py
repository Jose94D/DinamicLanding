import sqlite3

conexion = sqlite3.connect('database.db')
cursor = conexion.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS contenido_blog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    extracto TEXT NOT NULL,
    contenido TEXT NOT NULL,
    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conexion.commit()
conexion.close()
print("¡Tabla contenido_blog creada!")