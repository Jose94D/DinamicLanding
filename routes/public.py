from flask import Blueprint, render_template, request
from extensions import get_db_connection

public_bp = Blueprint('public', __name__)


@public_bp.before_request
def registrar_visita():
    """Registra cada visita a una página pública (para el módulo de Analíticas)."""
    conn = get_db_connection()
    conn.execute('INSERT INTO analiticas_visitas (ruta) VALUES (?)', (request.path,))
    conn.commit()
    conn.close()


@public_bp.route('/')
def index():
    conn = get_db_connection()
    seo = conn.execute('SELECT * FROM configuracion_seo WHERE id = 1').fetchone()
    modulos_activos = conn.execute('SELECT id FROM modulos WHERE activo = 1 ORDER BY orden ASC').fetchall()

    hero_data = conn.execute('SELECT * FROM contenido_hero WHERE id = 1').fetchone()
    carousel_data = conn.execute('SELECT * FROM contenido_carousel ORDER BY orden ASC').fetchall()
    services_data = conn.execute('SELECT * FROM contenido_services ORDER BY orden ASC').fetchall()
    gallery_data = conn.execute('SELECT * FROM contenido_gallery ORDER BY orden ASC').fetchall()
    testimonials_data = conn.execute('SELECT * FROM contenido_testimonials ORDER BY orden ASC').fetchall()
    blog_data = conn.execute('''
        SELECT * FROM contenido_blog WHERE activo = 1
        ORDER BY fecha_publicacion DESC LIMIT 3
    ''').fetchall()
    about_data = conn.execute('SELECT * FROM contenido_about WHERE id = 1').fetchone()

    conn.close()
    return render_template(
        'public/index.html',
        seo=seo,
        modulos=modulos_activos,
        hero=hero_data,
        carousel=carousel_data,
        services=services_data,
        gallery=gallery_data,
        testimonials=testimonials_data,
        blog=blog_data,
        about=about_data
    )


@public_bp.route('/articulo/<int:id>')
def ver_articulo(id):
    conn = get_db_connection()
    articulo = conn.execute('SELECT * FROM contenido_blog WHERE id = ?', (id,)).fetchone()
    conn.close()

    if not articulo:
        return "Artículo no encontrado", 404

    return render_template('public/post.html', articulo=articulo)