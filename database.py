import os
import secrets
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'database.db'


def inicializar_base_datos():
    conexion = sqlite3.connect(DB_PATH)
    conexion.execute('PRAGMA foreign_keys = ON')
    cursor = conexion.cursor()

    # ==========================================================
    # ADMINISTRACIÓN
    # ==========================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # ==========================================================
    # MÓDULOS DE LA LANDING (visibilidad + orden)
    # 'id' es un slug legible en texto (ej: 'hero', 'gallery')
    # que además es el nombre del archivo include en
    # templates/public/modulos/<id>.html
    # ==========================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modulos (
            id TEXT PRIMARY KEY,
            nombre_legible TEXT NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1,
            orden INTEGER NOT NULL
        )
    ''')

    # ==========================================================
    # CONTENIDO POR MÓDULO
    # ==========================================================

    # --- Hero (singleton: siempre id = 1) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contenido_hero (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            titulo TEXT NOT NULL,
            subtitulo TEXT,
            texto_boton TEXT,
            url_boton TEXT
        )
    ''')

    # --- Sobre Nosotros (singleton: siempre id = 1) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contenido_about (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            titulo TEXT NOT NULL,
            descripcion TEXT,
            mision TEXT
        )
    ''')

    # --- Carrusel (lista, con orden) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contenido_carousel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT NOT NULL,
            orden INTEGER NOT NULL DEFAULT 1
        )
    ''')

    # --- Servicios (lista, con orden) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contenido_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icono TEXT NOT NULL DEFAULT 'bi-star',
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            orden INTEGER NOT NULL DEFAULT 1
        )
    ''')

    # --- Galería (lista, con orden) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contenido_gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT NOT NULL,
            titulo TEXT,
            orden INTEGER NOT NULL DEFAULT 1
        )
    ''')

    # --- Testimonios (lista, con orden) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contenido_testimonials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cargo TEXT,
            texto TEXT NOT NULL,
            foto TEXT,
            calificacion INTEGER NOT NULL DEFAULT 5 CHECK (calificacion BETWEEN 1 AND 5),
            orden INTEGER NOT NULL DEFAULT 1
        )
    ''')

    # --- Blog (fusiona la vieja contenido_blog + blog_entradas) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contenido_blog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            extracto TEXT NOT NULL,
            contenido TEXT NOT NULL,
            imagen_portada TEXT,
            fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            activo INTEGER NOT NULL DEFAULT 1
        )
    ''')

    # ==========================================================
    # SEO (singleton: siempre id = 1)
    # ==========================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracion_seo (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            meta_titulo TEXT NOT NULL,
            meta_descripcion TEXT NOT NULL,
            og_image TEXT
        )
    ''')

    # ==========================================================
    # REDES SOCIALES (una fila por plataforma)
    # ==========================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracion_redes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plataforma TEXT UNIQUE NOT NULL,
            access_token TEXT,
            account_id TEXT,
            activo_api INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # ==========================================================
    # ANALÍTICAS DE VISITAS
    # ==========================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analiticas_visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            ruta TEXT NOT NULL
        )
    ''')
    # Índice para que las consultas de "visitas por año/mes" sean rápidas
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_analiticas_fecha ON analiticas_visitas (fecha)
    ''')

    # ==========================================================
    # MENSAJES DEL FORMULARIO DE CONTACTO
    # ==========================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes_contacto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
            leido INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # ==========================================================
    # DATOS POR DEFECTO
    # ==========================================================

    # Catálogo de módulos disponibles en la landing (orden inicial sugerido)
    modulos_default = [
        ('hero',         'Banner Principal (Hero)',            1),
        ('about',        'Sobre Nosotros',                     2),
        ('carousel',     'Carrusel de Imágenes',                3),
        ('services',     'Servicios',                           4),
        ('gallery',      'Galería de Productos',                5),
        ('testimonials', 'Testimonios de Clientes',             6),
        ('social',       'Módulo de Redes Sociales (Feed)',     7),
        ('blog_preview', 'Últimas Entradas del Blog',           8),
        ('contact',      'Formulario de Contacto',              9),
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO modulos (id, nombre_legible, activo, orden)
        VALUES (?, ?, 1, ?)
    ''', modulos_default)

    # Contenido inicial mínimo para que la landing no se vea vacía/rota
    cursor.execute('''
        INSERT OR IGNORE INTO contenido_hero (id, titulo, subtitulo, texto_boton, url_boton)
        VALUES (1, 'Bienvenido a tu Landing Page', 'Edita este texto desde el panel de administración', 'Contáctanos', '#contact')
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO contenido_about (id, titulo, descripcion, mision)
        VALUES (1, 'Sobre Nosotros', 'Cuenta aquí la historia de tu negocio.', 'Tu misión o propuesta de valor.')
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO configuracion_seo (id, meta_titulo, meta_descripcion)
        VALUES (1, 'Mi Landing Page', 'Descripción por defecto para motores de búsqueda')
    ''')

    # Usuario admin: por defecto usa ADMIN_USERNAME/ADMIN_PASSWORD del entorno
    # si están definidas. Si no, genera una contraseña aleatoria y la muestra
    # UNA sola vez en consola — no queda guardada en ningún archivo.
    cursor.execute('SELECT COUNT(*) FROM admin')
    if cursor.fetchone()[0] == 0:
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        password = os.environ.get('ADMIN_PASSWORD')
        password_generada = password is None
        if password_generada:
            password = secrets.token_urlsafe(12)

        cursor.execute('''
            INSERT INTO admin (username, password_hash) VALUES (?, ?)
        ''', (username, generate_password_hash(password)))

        if password_generada:
            print(
                "\n🔑 Se creó el usuario admin con una contraseña generada automáticamente:\n"
                f"    Usuario:    {username}\n"
                f"    Contraseña: {password}\n"
                "    Guárdala ahora — no se volverá a mostrar. Cámbiala en '/admin/cambiar-password'\n"
                "    después de tu primer inicio de sesión.\n"
            )

    conexion.commit()
    conexion.close()
    print("¡Base de datos SQLite generada con éxito!")


if __name__ == '__main__':
    inicializar_base_datos()