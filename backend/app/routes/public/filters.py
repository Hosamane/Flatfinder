from flask import jsonify
from app.routes.public import public_bp
from app.models.unit import Unit


@public_bp.route("/unit-filter-options", methods=["GET"])
def get_unit_filter_options():

    flat_types = Unit.__table__.columns.flat_type.type.enums
    furnishing_types = Unit.__table__.columns.furnishing.type.enums
    balcony_types = Unit.__table__.columns.balcony_type.type.enums

    return jsonify({
        "flat_types": flat_types,
        "furnishing_types": furnishing_types,
        "balcony_types": balcony_types
    })