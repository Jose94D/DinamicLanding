import os
from flask import Flask
from extensions import login_manager
from routes import register_blueprints

# ==========================================
# CARPETAS DE SUBIDA DE ARCHIVOS
# ==========================================
UPLOAD_FOLDERS = {
    'UPLOAD_FOLDER_CAROUSEL': 'static/uploads/carousel',
    'UPLOAD_FOLDER_GALLERY': 'static/uploads/gallery',
    'UPLOAD_FOLDER_TESTIMONIALS': 'static/uploads/testimonials',
}


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'una_clave_secreta_muy_segura'

    for key, path in UPLOAD_FOLDERS.items():
        app.config[key] = path
        os.makedirs(path, exist_ok=True)

    login_manager.init_app(app)
    register_blueprints(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)