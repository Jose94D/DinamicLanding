from .public import public_bp
from .auth import auth_bp
from .dashboard import dashboard_bp
from .content import content_bp
from .seo import seo_bp
from .analytics import analytics_bp


def register_blueprints(app):
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(seo_bp)
    app.register_blueprint(analytics_bp)