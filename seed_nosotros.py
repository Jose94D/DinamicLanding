import sqlite3

conexion = sqlite3.connect('database.db')
cursor = conexion.cursor()

# Usamos CHECK (id = 1) para asegurar que solo exista un registro de configuración
cursor.execute('''
CREATE TABLE IF NOT EXISTS contenido_nosotros (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    mision TEXT
)
''')

# Insertamos los valores por defecto si no existen
cursor.execute('''
INSERT OR IGNORE INTO contenido_nosotros (id, titulo, descripcion, mision) 
VALUES (1, 'Sobre Nosotros', 'Describe aquí tu historia o propuesta de valor.', 'Nuestra misión principal...')
''')

conexion.commit()
conexion.close()
print("¡Tabla contenido_nosotros creada!")