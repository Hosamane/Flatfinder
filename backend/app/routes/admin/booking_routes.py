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
            "exitedBeforeLeaseEnd": b.exitedBeforeLeaseEnd,
            "status": b.status
        }
        for b in bookings
    ])



@admin_bp.route("/bookings/<int:id>", methods=["PUT"])
@admin_required
def update_booking_status(id):

    data = request.get_json()
    new_status = data.get("status")
    #left beforelease expiry
    # left_before = data.get("exitedBeforeLLeaseEnd")


    booking = Booking.query.get_or_404(id)

    # if left_before not in [True, False]:
    #     return jsonify({"error": "Invalid value for exitedBeforeLeaseEnd"}), 400
    if new_status not in ["APPROVED", "REJECTED"]:
        return jsonify({"error": "Invalid status"}), 400
    

    booking.status = new_status

    if(booking.status == "APPROVED"):
        booking.unit.available_from = booking.lease_end
    # booking.exitedBeforeLeaseEnd = left_before
    db.session.commit()

    return jsonify({"message": "Booking updated"})



@admin_bp.route("/bookings/<int:id>/move-out",methods=["POST"])
@admin_required
def vacate_booking(id):
    booking = Booking.query.get_or_404(id)

    if booking.status != "APPROVED":
        return jsonify({"error":"Only approved bookings can be vacated"}), 400
    
    if booking.actual_move_out_date:    
        return jsonify({"error": "Tenant already moved out"}), 400
    data = request.get_json()
    vacate_date_str = data.get("vacate_date")

    if not vacate_date_str:
        return jsonify({"error": "vacate_date is required"}), 400
    
    vacate_date = datetime.strptime(vacate_date_str, "%Y-%m-%d").date()

    today = datetime.today().date() 

    if vacate_date < today:
        return jsonify({"error":"vacate can't be done in past"}), 400
    
    if vacate_date < booking.lease_start:
        return jsonify({"error":"vacate date cannot be before lease start date"}), 400
    
    if vacate_date > booking.lease_end:
        return jsonify({"error":"vacate date cannot be after lease end date"}), 400
    
    booking.actual_move_out_date = vacate_date

    if vacate_date< booking.lease_end:
        booking.exitedBeforeLeaseEnd = True


    booking.unit.available_from = vacate_date

    booking.status = "COMPLETED"

    db.session.commit()

    return jsonify({"message": "vacate date updated successfully"})



# @admin_bp.route("/bookings/<int:id>/cancel",methods=["POST"])
# @admin_required
# def cancel_booking(id):
#     print("Cancel booking called for id:", id)

#     booking = Booking.query.get_or_404(id)

#     if booking.status != "APPROVED":
#         return jsonify({"error":"only approved bookings can be cancelled"}), 400
    

#     today = datetime.today().date()

#     if today >= booking.lease_start:
#         return jsonify({"error":"Lease already started, can't cancel. Use move-out instead"}), 400
    
#     booking.status = "CANCELLED"

#     booking.unit.available_from = today

#     db.session.commit()

#     return jsonify({"message":"booking cancelled successfully"})