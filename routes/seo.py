from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import get_db_connection

seo_bp = Blueprint('seo', __name__, url_prefix='/admin')


@seo_bp.route('/seo', methods=['GET', 'POST'])
@login_required
def editar_seo():
    conn = get_db_connection()
    if request.method == 'POST':
        meta_titulo = request.form['meta_titulo']
        meta_descripcion = request.form['meta_descripcion']
        og_image = request.form.get('og_image', '')

        conn.execute('''
            UPDATE configuracion_seo
            SET meta_titulo = ?, meta_descripcion = ?, og_image = ?
            WHERE id = 1
        ''', (meta_titulo, meta_descripcion, og_image))
        conn.commit()
        flash("Configuración SEO actualizada.", "success")
        return redirect(url_for('seo.editar_seo'))

    seo = conn.execute('SELECT * FROM configuracion_seo WHERE id = 1').fetchone()
    conn.close()
    return render_template('admin/editar_seo.html', seo=seo)