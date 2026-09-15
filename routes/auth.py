from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from extensions import get_db_connection, User

auth_bp = Blueprint('auth', __name__, url_prefix='/admin')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM admin WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template('admin/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))