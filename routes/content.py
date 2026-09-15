import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from extensions import get_db_connection
from utils import generar_slug

content_bp = Blueprint('content', __name__, url_prefix='/admin/contenido')


# ==========================================
# HERO
# ==========================================
@content_bp.route('/hero', methods=['GET', 'POST'])
@login_required
def editar_hero():
    conn = get_db_connection()
    if request.method == 'POST':
        titulo = request.form['titulo']
        subtitulo = request.form['subtitulo']
        texto_boton = request.form['texto_boton']
        url_boton = request.form['url_boton']

        conn.execute('''
            UPDATE contenido_hero
            SET titulo = ?, subtitulo = ?, texto_boton = ?, url_boton = ?
            WHERE id = 1
        ''', (titulo, subtitulo, texto_boton, url_boton))
        conn.commit()
        flash("¡Contenido del Hero actualizado!", "success")
        return redirect(url_for('content.editar_hero'))

    hero_data = conn.execute('SELECT * FROM contenido_hero WHERE id = 1').fetchone()
    conn.close()
    return render_template('admin/editar_hero.html', hero=hero_data)


# ==========================================
# SOBRE NOSOTROS
# ==========================================
@content_bp.route('/about', methods=['GET', 'POST'])
@login_required
def editar_about():
    conn = get_db_connection()
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        mision = request.form['mision']

        conn.execute('''
            UPDATE contenido_about
            SET titulo = ?, descripcion = ?, mision = ?
            WHERE id = 1
        ''', (titulo, descripcion, mision))
        conn.commit()
        flash("Sección Sobre Nosotros actualizada.", "success")
        return redirect(url_for('content.editar_about'))

    nosotros = conn.execute('SELECT * FROM contenido_about WHERE id = 1').fetchone()
    conn.close()
    return render_template('admin/editar_about.html', nosotros=nosotros)


# ==========================================
# CARRUSEL
# ==========================================
@content_bp.route('/carousel', methods=['GET', 'POST'])
@login_required
def editar_carousel():
    conn = get_db_connection()

    if request.method == 'POST':
        if 'imagen' not in request.files:
            flash("No se seleccionó ningún archivo", "danger")
            return redirect(request.url)

        file = request.files['imagen']
        if file.filename == '':
            flash("El archivo no tiene nombre", "danger")
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER_CAROUSEL'], filename)
            file.save(filepath)

            conn.execute('INSERT INTO contenido_carousel (nombre_archivo) VALUES (?)', (filename,))
            conn.commit()
            flash("Imagen subida con éxito", "success")
            return redirect(url_for('content.editar_carousel'))

    imagenes = conn.execute('SELECT * FROM contenido_carousel ORDER BY orden ASC').fetchall()
    conn.close()
    return render_template('admin/editar_carousel.html', imagenes=imagenes)


@content_bp.route('/carousel/eliminar/<int:id>')
@login_required
def eliminar_carousel(id):
    conn = get_db_connection()
    img = conn.execute('SELECT nombre_archivo FROM contenido_carousel WHERE id = ?', (id,)).fetchone()

    if img:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER_CAROUSEL'], img['nombre_archivo'])
        if os.path.exists(filepath):
            os.remove(filepath)

        conn.execute('DELETE FROM contenido_carousel WHERE id = ?', (id,))
        conn.commit()
        flash("Imagen eliminada.", "success")

    conn.close()
    return redirect(url_for('content.editar_carousel'))


# ==========================================
# SERVICIOS
# ==========================================
@content_bp.route('/servicios', methods=['GET', 'POST'])
@login_required
def editar_servicios():
    conn = get_db_connection()
    if request.method == 'POST':
        icono = request.form['icono']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        orden = request.form.get('orden', 1, type=int)

        conn.execute('INSERT INTO contenido_services (icono, titulo, descripcion, orden) VALUES (?, ?, ?, ?)',
                     (icono, titulo, descripcion, orden))
        conn.commit()
        flash("Servicio agregado exitosamente.", "success")
        return redirect(url_for('content.editar_servicios'))

    servicios = conn.execute('SELECT * FROM contenido_services ORDER BY orden ASC').fetchall()
    conn.close()
    return render_template('admin/editar_servicios.html', servicios=servicios)


@content_bp.route('/servicios/eliminar/<int:id>')
@login_required
def eliminar_servicio(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contenido_services WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Servicio eliminado.", "success")
    return redirect(url_for('content.editar_servicios'))


# ==========================================
# GALERÍA
# ==========================================
@content_bp.route('/gallery', methods=['GET', 'POST'])
@login_required
def editar_gallery():
    conn = get_db_connection()

    if request.method == 'POST':
        if 'imagen' not in request.files or request.files['imagen'].filename == '':
            flash("No se seleccionó ningún archivo", "danger")
            return redirect(request.url)

        file = request.files['imagen']
        titulo = request.form.get('titulo', '')
        orden = request.form.get('orden', 1, type=int)

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER_GALLERY'], filename)
        file.save(filepath)

        conn.execute(
            'INSERT INTO contenido_gallery (nombre_archivo, titulo, orden) VALUES (?, ?, ?)',
            (filename, titulo, orden)
        )
        conn.commit()
        flash("Imagen agregada a la galería.", "success")
        return redirect(url_for('content.editar_gallery'))

    items = conn.execute('SELECT * FROM contenido_gallery ORDER BY orden ASC').fetchall()
    conn.close()
    return render_template('admin/editar_gallery.html', items=items)


@content_bp.route('/gallery/eliminar/<int:id>')
@login_required
def eliminar_gallery(id):
    conn = get_db_connection()
    item = conn.execute('SELECT nombre_archivo FROM contenido_gallery WHERE id = ?', (id,)).fetchone()

    if item:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER_GALLERY'], item['nombre_archivo'])
        if os.path.exists(filepath):
            os.remove(filepath)
        conn.execute('DELETE FROM contenido_gallery WHERE id = ?', (id,))
        conn.commit()
        flash("Imagen eliminada de la galería.", "success")

    conn.close()
    return redirect(url_for('content.editar_gallery'))


# ==========================================
# TESTIMONIOS
# ==========================================
@content_bp.route('/testimonials', methods=['GET', 'POST'])
@login_required
def editar_testimonials():
    conn = get_db_connection()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cargo = request.form.get('cargo', '')
        texto = request.form['texto']
        calificacion = request.form.get('calificacion', 5, type=int)
        orden = request.form.get('orden', 1, type=int)

        foto_filename = None
        file = request.files.get('foto')
        if file and file.filename != '':
            foto_filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER_TESTIMONIALS'], foto_filename))

        conn.execute('''
            INSERT INTO contenido_testimonials (nombre, cargo, texto, foto, calificacion, orden)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, cargo, texto, foto_filename, calificacion, orden))
        conn.commit()
        flash("Testimonio agregado exitosamente.", "success")
        return redirect(url_for('content.editar_testimonials'))

    testimonios = conn.execute('SELECT * FROM contenido_testimonials ORDER BY orden ASC').fetchall()
    conn.close()
    return render_template('admin/editar_testimonials.html', testimonios=testimonios)


@content_bp.route('/testimonials/eliminar/<int:id>')
@login_required
def eliminar_testimonial(id):
    conn = get_db_connection()
    item = conn.execute('SELECT foto FROM contenido_testimonials WHERE id = ?', (id,)).fetchone()

    if item and item['foto']:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER_TESTIMONIALS'], item['foto'])
        if os.path.exists(filepath):
            os.remove(filepath)

    conn.execute('DELETE FROM contenido_testimonials WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Testimonio eliminado.", "success")
    return redirect(url_for('content.editar_testimonials'))


# ==========================================
# BLOG
# ==========================================
@content_bp.route('/blog', methods=['GET', 'POST'])
@login_required
def editar_blog():
    conn = get_db_connection()
    if request.method == 'POST':
        titulo = request.form['titulo']
        extracto = request.form['extracto']
        contenido = request.form['contenido']

        slug_base = generar_slug(titulo)
        existe = conn.execute('SELECT id FROM contenido_blog WHERE slug = ?', (slug_base,)).fetchone()
        slug = slug_base if not existe else f"{slug_base}-{os.urandom(2).hex()}"

        conn.execute(
            'INSERT INTO contenido_blog (titulo, slug, extracto, contenido) VALUES (?, ?, ?, ?)',
            (titulo, slug, extracto, contenido)
        )
        conn.commit()
        flash("Artículo publicado exitosamente.", "success")
        return redirect(url_for('content.editar_blog'))

    articulos = conn.execute('SELECT * FROM contenido_blog ORDER BY fecha_publicacion DESC').fetchall()
    conn.close()
    return render_template('admin/editar_blog.html', articulos=articulos)


@content_bp.route('/blog/eliminar/<int:id>')
@login_required
def eliminar_articulo(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contenido_blog WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Artículo eliminado.", "success")
    return redirect(url_for('content.editar_blog'))