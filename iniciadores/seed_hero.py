import sqlite3

conexion = sqlite3.connect('database.db')
cursor = conexion.cursor()

# Crear tabla específica para el contenido del Hero
cursor.execute('''
CREATE TABLE IF NOT EXISTS contenido_hero (
    id INTEGER PRIMARY KEY,
    titulo TEXT,
    subtitulo TEXT,
    texto_boton TEXT,
    url_boton TEXT
)
''')

# Insertar el contenido por defecto si la tabla está vacía
cursor.execute("SELECT COUNT(*) FROM contenido_hero")
if cursor.fetchone()[0] == 0:
    cursor.execute('''
    INSERT INTO contenido_hero (titulo, subtitulo, texto_boton, url_boton) 
    VALUES (?, ?, ?, ?)
    ''', ('Bienvenido a nuestro sistema', 'Una solución modular, rápida y autogestionable.', 'Conocer más', '#'))

conexion.commit()
conexion.close()
print("¡Tabla contenido_hero creada y poblada!")