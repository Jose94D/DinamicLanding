import sqlite3
from flask_login import LoginManager, UserMixin

DB_PATH = 'database.db'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_row = conn.execute('SELECT * FROM admin WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_row:
        return User(user_row['id'], user_row['username'])
    return None