from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions.jwt import jwt
from app.models import Booking, Unit
from app.extensions import db
from datetime import datetime

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/", methods=["POST"])
@jwt_required()
def create_booking():

    user_id = get_jwt_identity()

    data = request.get_json()

    unit_code = data.get("unit_code")
    lease_start = datetime.strptime(data.get("lease_start"), "%Y-%m-%d").date()
    lease_end = datetime.strptime(data.get("lease_end"), "%Y-%m-%d").date()

    unit = Unit.query.filter_by(unit_code=unit_code).first()

    if not unit:
        return jsonify({"error": "Unit not found"}), 404

    if (lease_end - lease_start).days < 30:
        return jsonify({"error": "Minimum lease duration is 30 days"}), 400

    booking = Booking(
        user_id=user_id,
        unit_id=unit.id,
        move_in_date=lease_start,
        lease_start=lease_start,
        lease_end=lease_end,
        status="PENDING",
        rent_snapshot=unit.rent
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({"message": "Booking request sent"}), 201




@booking_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_bookings():

    user_id = get_jwt_identity()

    bookings = Booking.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": b.id,
            "unit_code": b.unit.unit_code,
            "lease_start": b.lease_start.isoformat(),
            "lease_end": b.lease_end.isoformat(),
            "status": b.status
        }
        for b in bookings
    ])
