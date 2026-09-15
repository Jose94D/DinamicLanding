from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import get_db_connection

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/admin')


@dashboard_bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    conn = get_db_connection()

    if request.method == 'POST':
        modulos_db = conn.execute('SELECT id FROM modulos').fetchall()
        for mod in modulos_db:
            mod_id = mod['id']
            activo = 1 if request.form.get(f'activo_{mod_id}') else 0
            orden = request.form.get(f'orden_{mod_id}', type=int)

            conn.execute('UPDATE modulos SET activo = ?, orden = ? WHERE id = ?', (activo, orden, mod_id))

        conn.commit()
        flash("¡Configuración de módulos actualizada exitosamente!", "success")
        return redirect(url_for('dashboard.dashboard'))

    modulos = conn.execute('SELECT * FROM modulos ORDER BY orden ASC').fetchall()
    conn.close()

    return render_template('admin/dashboard.html', modulos=modulos)