import sqlite3

conexion = sqlite3.connect('database.db')
cursor = conexion.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS contenido_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    icono TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    orden INTEGER DEFAULT 1
)
''')

conexion.commit()
conexion.close()
print("¡Tabla contenido_services creada!")