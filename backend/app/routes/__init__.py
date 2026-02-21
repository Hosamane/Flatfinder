from .auth_routes import auth_bp
from .unit_routes import unit_bp
from .booking_routes import booking_bp
# from .admin_routes import admin_bp
# from .admin.tower_routes import admin_bp 
from .admin import admin_bp
from .public import public_bp
from .tenant_profile import tenant_bp
def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(unit_bp, url_prefix="/api/units")
    app.register_blueprint(booking_bp, url_prefix="/api/bookings")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(public_bp,url_prefix="/api/public")
    app.register_blueprint(tenant_bp,url_prefix="/api/tenant")