import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

# ==========================================
# 1. INICIALIZACIÓN Y CONFIGURACIÓN
# ==========================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_clave_secreta_muy_segura'

# Configuración y creación de carpetas de subida
app.config['UPLOAD_FOLDER_CAROUSEL'] = 'static/uploads/carousel'
os.makedirs(app.config['UPLOAD_FOLDER_CAROUSEL'], exist_ok=True)

# ==========================================
# 2. CONFIGURACIÓN DE FLASK-LOGIN
# ==========================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirige aquí si no está logueado
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."

# ==========================================
# 3. MODELOS Y BASE DE DATOS
# ==========================================
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

def get_db_connection():
    conn = sqlite3.connect('database.db')
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

# ==========================================
# 4. RUTAS PÚBLICAS (FRONTEND)
# ==========================================
@app.route('/')
def index():
    conn = get_db_connection()
    seo = conn.execute('SELECT * FROM configuracion_seo WHERE id = 1').fetchone()
    modulos_activos = conn.execute('SELECT id FROM modulos WHERE activo = 1 ORDER BY orden ASC').fetchall()
    
    hero_data = conn.execute('SELECT * FROM contenido_hero WHERE id = 1').fetchone()
    carousel_data = conn.execute('SELECT * FROM contenido_carousel ORDER BY orden ASC').fetchall()
    services_data = conn.execute('SELECT * FROM contenido_servicios ORDER BY orden ASC').fetchall()
    
    conn.close()
    return render_template('public/index.html', seo=seo, modulos=modulos_activos, hero=hero_data, carousel=carousel_data, services=services_data)
# ==========================================
# 5. RUTAS DE AUTENTICACIÓN
# ==========================================
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM admin WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ==========================================
# 6. RUTAS DEL DASHBOARD (ADMINISTRACIÓN GENERAL)
# ==========================================
@app.route('/admin/', methods=['GET', 'POST'])
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
        return redirect(url_for('dashboard'))

    modulos = conn.execute('SELECT * FROM modulos ORDER BY orden ASC').fetchall()
    conn.close()
    
    return render_template('admin/dashboard.html', modulos=modulos)

# ==========================================
# 7. RUTAS DE GESTIÓN DE CONTENIDO (MÓDULOS)
# ==========================================
@app.route('/admin/contenido/hero', methods=['GET', 'POST'])
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
        return redirect(url_for('editar_hero'))
        
    hero_data = conn.execute('SELECT * FROM contenido_hero WHERE id = 1').fetchone()
    conn.close()
    return render_template('admin/editar_hero.html', hero=hero_data)

@app.route('/admin/contenido/carousel', methods=['GET', 'POST'])
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
            filepath = os.path.join(app.config['UPLOAD_FOLDER_CAROUSEL'], filename)
            file.save(filepath)
            
            conn.execute('INSERT INTO contenido_carousel (nombre_archivo) VALUES (?)', (filename,))
            conn.commit()
            flash("Imagen subida con éxito", "success")
            return redirect(url_for('editar_carousel'))

    imagenes = conn.execute('SELECT * FROM contenido_carousel ORDER BY orden ASC').fetchall()
    conn.close()
    return render_template('admin/editar_carousel.html', imagenes=imagenes)

@app.route('/admin/contenido/carousel/eliminar/<int:id>')
@login_required
def eliminar_carousel(id):
    conn = get_db_connection()
    img = conn.execute('SELECT nombre_archivo FROM contenido_carousel WHERE id = ?', (id,)).fetchone()
    
    if img:
        filepath = os.path.join(app.config['UPLOAD_FOLDER_CAROUSEL'], img['nombre_archivo'])
        if os.path.exists(filepath):
            os.remove(filepath)
        
        conn.execute('DELETE FROM contenido_carousel WHERE id = ?', (id,))
        conn.commit()
        flash("Imagen eliminada.", "success")
        
    conn.close()
    return redirect(url_for('editar_carousel'))

@app.route('/admin/contenido/servicios', methods=['GET', 'POST'])
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
        return redirect(url_for('editar_servicios'))
        
    servicios = conn.execute('SELECT * FROM contenido_services ORDER BY orden ASC').fetchall()
    conn.close()
    return render_template('admin/editar_servicios.html', servicios=servicios)

@app.route('/admin/contenido/servicios/eliminar/<int:id>')
@login_required
def eliminar_servicio(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contenido_services WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Servicio eliminado.", "success")
    return redirect(url_for('editar_servicios'))

# ==========================================
# 8. ARRANQUE DE LA APLICACIÓN
# ==========================================
if __name__ == '__main__':
    app.run(debug=True)