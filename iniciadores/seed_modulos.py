import sqlite3

modulos_iniciales = [
    ('hero', 'Banner Principal (Hero)', 1, 1),
    ('about', 'Sobre Nosotros', 1, 2),
    ('services', 'Servicios', 1, 3),
    ('gallery', 'Galería de Productos', 1, 4),
    ('carousel', 'Carrusel de Imágenes', 1, 5),
    ('testimonials', 'Testimonios de Clientes', 1, 6),
    ('social', 'Módulo de Redes Sociales (Feed)', 1, 7),
    ('blog_preview', 'Últimas Entradas del Blog', 1, 8),
    ('contact', 'Formulario de Contacto', 1, 9)
]

conexion = sqlite3.connect('database.db')
cursor = conexion.cursor()

for mod in modulos_iniciales:
    try:
        cursor.execute("INSERT INTO modulos (id, nombre_legible, activo, orden) VALUES (?, ?, ?, ?)", mod)
    except sqlite3.IntegrityError:
        pass # Si el módulo ya existe, lo ignoramos

conexion.commit()
conexion.close()
print("¡Módulos base insertados correctamente en la base de datos!")