import sqlite3

conexion = sqlite3.connect('database.db')
cursor = conexion.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS contenido_carousel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_archivo TEXT NOT NULL,
    orden INTEGER DEFAULT 1
)
''')

conexion.commit()
conexion.close()
print("¡Tabla contenido_carousel creada!")