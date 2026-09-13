import sqlite3

def inicializar_base_datos():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS configuracion_seo (id INTEGER PRIMARY KEY AUTOINCREMENT, meta_title TEXT NOT NULL, meta_description TEXT NOT NULL, og_image TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS modulos (id TEXT PRIMARY KEY, nombre_legible TEXT NOT NULL, activo INTEGER NOT NULL DEFAULT 1, orden INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS contenidos_landing (id INTEGER PRIMARY KEY AUTOINCREMENT, modulo_id TEXT, clave_campo TEXT NOT NULL, valor TEXT, FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS configuracion_redes (id INTEGER PRIMARY KEY AUTOINCREMENT, plataforma TEXT NOT NULL, access_token TEXT, account_id TEXT, activo_api INTEGER NOT NULL DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS blog_entradas (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, slug TEXT UNIQUE NOT NULL, contenido TEXT NOT NULL, imagen_portada TEXT, fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP, activo INTEGER NOT NULL DEFAULT 1)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS analiticas_visitas (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ruta TEXT NOT NULL)''')

    # Insertar configuración SEO por defecto
    cursor.execute("INSERT OR IGNORE INTO configuracion_seo (id, meta_title, meta_description) VALUES (1, 'Mi Landing Page', 'Descripción por defecto')")

    conexion.commit()
    conexion.close()
    print("¡Base de datos SQLite generada con éxito!")

if __name__ == '__main__':
    inicializar_base_datos()