import os
import secrets
from flask import Flask
from flask_login import current_user
from extensions import login_manager, get_db_connection
from routes import register_blueprints

# ==========================================
# CARPETAS DE SUBIDA DE ARCHIVOS
# ==========================================
UPLOAD_FOLDERS = {
    'UPLOAD_FOLDER_CAROUSEL': 'static/uploads/carousel',
    'UPLOAD_FOLDER_GALLERY': 'static/uploads/gallery',
    'UPLOAD_FOLDER_TESTIMONIALS': 'static/uploads/testimonials',
}


def _resolver_secret_key():
    """
    Usa SECRET_KEY del entorno si está definida. Si no, genera una temporal
    y advierte: una clave temporal cambia en cada reinicio del servidor,
    lo que invalida sesiones activas y cookies "recordarme". NO usar así en producción.
    """
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        secret_key = secrets.token_hex(32)
        print(
            "\n⚠️  ADVERTENCIA: no definiste la variable de entorno SECRET_KEY.\n"
            "    Se generó una temporal para esta ejecución. Cambiará en cada\n"
            "    reinicio (cerrando sesiones activas). Define SECRET_KEY en tu\n"
            "    entorno antes de desplegar a producción. Ejemplo:\n"
            "        export SECRET_KEY=$(python3 -c \"import secrets; print(secrets.token_hex(32))\")\n"
        )
    return secret_key


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = _resolver_secret_key()

    for key, path in UPLOAD_FOLDERS.items():
        app.config[key] = path
        os.makedirs(path, exist_ok=True)

    login_manager.init_app(app)
    register_blueprints(app)

    @app.context_processor
    def inyectar_mensajes_no_leidos():
        """Hace disponible 'no_leidos_sidebar' en TODOS los templates (usado en _sidebar.html)."""
        if current_user.is_authenticated:
            conn = get_db_connection()
            total = conn.execute(
                'SELECT COUNT(*) as total FROM mensajes_contacto WHERE leido = 0'
            ).fetchone()['total']
            conn.close()
            return {'no_leidos_sidebar': total}
        return {'no_leidos_sidebar': 0}

    return app


app = create_app()

if __name__ == '__main__':
    # DEBUG=1 lo activa; por defecto queda APAGADO (nunca actives esto en producción,
    # el modo debug de Flask expone un debugger interactivo que ejecuta código arbitrario).
    modo_debug = os.environ.get('DEBUG', '1') == '1'
    app.run(debug=modo_debug)