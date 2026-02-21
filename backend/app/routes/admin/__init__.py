from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

from . import tower_routes
from . import unit_routes
from . import bulk_unit_creation
from . import booking_routes
from . import images_routes
from . import csv_upload
from . import dashboard
