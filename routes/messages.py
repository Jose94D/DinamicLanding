from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from extensions import get_db_connection

messages_bp = Blueprint('messages', __name__, url_prefix='/admin/mensajes')


@messages_bp.route('/')
@login_required
def listar_mensajes():
    conn = get_db_connection()
    mensajes = conn.execute(
        'SELECT * FROM mensajes_contacto ORDER BY fecha_envio DESC'
    ).fetchall()
    no_leidos = conn.execute(
        'SELECT COUNT(*) as total FROM mensajes_contacto WHERE leido = 0'
    ).fetchone()['total']
    conn.close()
    return render_template('admin/mensajes.html', mensajes=mensajes, no_leidos=no_leidos)


@messages_bp.route('/marcar_leido/<int:id>')
@login_required
def marcar_leido(id):
    conn = get_db_connection()
    conn.execute('UPDATE mensajes_contacto SET leido = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('messages.listar_mensajes'))


@messages_bp.route('/eliminar/<int:id>')
@login_required
def eliminar_mensaje(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM mensajes_contacto WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Mensaje eliminado.", "success")
    return redirect(url_for('messages.listar_mensajes'))