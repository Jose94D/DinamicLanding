from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import get_db_connection
from social_api import invalidar_cache

social_bp = Blueprint('social', __name__, url_prefix='/admin/redes')

PLATAFORMAS_SOPORTADAS = ['instagram']


@social_bp.route('/', methods=['GET', 'POST'])
@login_required
def editar_redes():
    conn = get_db_connection()

    if request.method == 'POST':
        plataforma = request.form['plataforma']
        access_token = request.form.get('access_token', '').strip()
        account_id = request.form.get('account_id', '').strip()
        activo_api = 1 if request.form.get('activo_api') else 0

        if plataforma not in PLATAFORMAS_SOPORTADAS:
            flash("Plataforma no soportada.", "danger")
            return redirect(url_for('social.editar_redes'))

        conn.execute('''
            INSERT INTO configuracion_redes (plataforma, access_token, account_id, activo_api)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(plataforma) DO UPDATE SET
                access_token = excluded.access_token,
                account_id = excluded.account_id,
                activo_api = excluded.activo_api
        ''', (plataforma, access_token, account_id, activo_api))
        conn.commit()

        invalidar_cache(account_id)
        flash(f"Configuración de {plataforma.capitalize()} guardada.", "success")
        return redirect(url_for('social.editar_redes'))

    redes = conn.execute('SELECT * FROM configuracion_redes').fetchall()
    conn.close()

    # Arma un dict {plataforma: fila} para precargar el formulario fácilmente
    redes_por_plataforma = {r['plataforma']: r for r in redes}

    return render_template(
        'admin/editar_redes.html',
        redes=redes,
        redes_por_plataforma=redes_por_plataforma,
        plataformas=PLATAFORMAS_SOPORTADAS
    )


@social_bp.route('/desactivar/<plataforma>')
@login_required
def desactivar_red(plataforma):
    conn = get_db_connection()
    conn.execute('UPDATE configuracion_redes SET activo_api = 0 WHERE plataforma = ?', (plataforma,))
    conn.commit()
    conn.close()
    flash(f"{plataforma.capitalize()} desactivado.", "success")
    return redirect(url_for('social.editar_redes'))