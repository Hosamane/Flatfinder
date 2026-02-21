from flask import request, jsonify
from app.routes.admin import admin_bp
from app.utils.decorators import admin_required
from app.services.bulk_unit_service import (
    bulk_create_units_list,
    bulk_create_by_range
)
from datetime import datetime
from app.models import Unit
# from app.services.tower_service import get_tower_id_by_code
from app.extensions import db

@admin_bp.route("/towers/<string:code>/units/bulk", methods=["POST"])
@admin_required
def bulk_add_units(code):
    try:
        data = request.get_json()

        if "units" in data:
            units = bulk_create_units_list(code, data)
        else:
            units = bulk_create_by_range(code, data)

        return jsonify({
            "created_count": len(units),
            "units": [u.unit_code for u in units]
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
