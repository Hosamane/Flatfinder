from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions.jwt import jwt
from app.models import Booking, Unit
from app.extensions import db
from app.routes.admin import admin_bp
from datetime import datetime

from app.utils.decorators import admin_required


@admin_bp.route("/bookings", methods=["GET"])
@admin_required
def get_all_bookings():

    bookings = Booking.query.all()

    return jsonify([
        {
            "id": b.id,
            "user": b.user.name,
            "unit_code": b.unit.unit_code,
            "lease_start": b.lease_start.isoformat(),
            "lease_end": b.lease_end.isoformat(),
            "status": b.status
        }
        for b in bookings
    ])



@admin_bp.route("/bookings/<int:id>", methods=["PUT"])
@admin_required
def update_booking_status(id):

    data = request.get_json()
    new_status = data.get("status")

    booking = Booking.query.get_or_404(id)

    if new_status not in ["APPROVED", "REJECTED"]:
        return jsonify({"error": "Invalid status"}), 400

    booking.status = new_status
    db.session.commit()

    return jsonify({"message": "Booking updated"})
