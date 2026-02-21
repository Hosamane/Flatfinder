from flask import Blueprint, request, jsonify
from app.services.unit_service import get_filtered_units
from datetime import datetime

unit_bp = Blueprint("units", __name__)


@unit_bp.route("/", methods=["GET"])
def list_units():

    filters = {
        "flat_type": request.args.get("flat_type"),
        "furnishing": request.args.get("furnishing"),
        "balcony_type": request.args.get("balcony_type"),
        "facing_direction": request.args.get("facing_direction"),
        "locality": request.args.get("locality"),
        "sort": request.args.get("sort"),
    }

    # Parking conversion
    parking = request.args.get("parking")
    if parking is not None:
        filters["parking"] = parking.lower() == "true"

    # Move-in date
    move_in = request.args.get("move_in_date")
    if move_in:
        filters["move_in_date"] = datetime.strptime(
            move_in, "%Y-%m-%d"
        ).date()

    units = get_filtered_units(filters)

    response = [
        {
            "unit_code": u.unit_code,
            "rent": str(u.rent),
            "available_from": u.available_from,
            "flat_type": u.flat_type,
            "locality": u.tower.locality,
            "image": u.image.cloudinary_url if u.image else None
        }
        for u in units
    ]

    return jsonify(response)
