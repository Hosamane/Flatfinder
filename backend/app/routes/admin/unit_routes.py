from flask import request,jsonify
from app.routes.admin import admin_bp
from app.utils.decorators import admin_required
from app.services.unit_service import (
    create_unit,
    get_units_by_tower,
    delete_unit
)
from app.models import Unit, Booking
from app.extensions import db
from datetime import date

@admin_bp.route("/towers/<string:code>/units",methods=["POST"])
@admin_required
def add_unit(code):
    try:
        data = request.get_json()
        unit = create_unit(code,data)

        return jsonify({ 
            "unit code":unit.unit_code,
            "wing":unit.wing,
            "flat_number":unit.flat_number,
            "rent":str(unit.rent),
            "Available from":unit.available_from,
            "flat_type":unit.flat_type,
            "furnishing":unit.furnishing,
            "balcony_type":unit.balcony_type,
            "parking":unit.parking,
            "facing_direction":unit.facing_direction
        }) ,201 
    except Exception as e:
        return jsonify({"error":str(e)}),400
    

@admin_bp.route("/towers/<string:code>/units",methods=["GET"])
@admin_required
def list_units(code):
    try:
        units = get_units_by_tower(code)

        return jsonify(
            [
            {
                "Tower id":unit.tower_id,
                "id":unit.id,
                 "unit code":unit.unit_code,
            "wing":unit.wing,
            "flat_number":unit.flat_number,
            "rent":str(unit.rent),
            "Available from":unit.available_from,
            "flat_type":unit.flat_type,
            "furnishing":unit.furnishing,
            "balcony_type":unit.balcony_type,
            "parking":unit.parking,
            "facing_direction":unit.facing_direction
            }
            for unit in units
        ]),200

    except Exception as e:
        return jsonify({"error":str(e)}),400
    


@admin_bp.route("/units/<string:unit_code>",methods=["DELETE"])
@admin_required
def remove_unit(unit_code):
    try:
        delete_unit(unit_code)
        return jsonify({"message":"Unit deleted"}),200
    except Exception as e:
        return jsonify({"error":str(e)}),400
    
from app.services.unit_service import update_unit

#update unit
@admin_bp.route("/units/<string:unit_code>",methods=["PUT"])
@admin_required
def edit_unit(unit_code):
    try:
        data = request.get_json()

        unit=update_unit(unit_code,data)

        return jsonify({
            "unit id":unit.id,
            "tower code":unit.tower.code,
            "unit code":unit.unit_code,
            "wing":unit.wing,
            "flat_number":unit.flat_number,         
            "rent":str(unit.rent),
            "Available from":unit.available_from,
            "flat_type":unit.flat_type,
            "furnishing":unit.furnishing,
            "balcony_type":unit.balcony_type,
            "parking":unit.parking,
            "facing_direction":unit.facing_direction,
            "is_active":unit.is_active
        }),200
    
    except Exception as e:
        return jsonify({"error":str(e)}),400
    
from app.services.occupancy_service import is_unit_occupied_by_code


@admin_bp.route("/units/<string:unit_code>/occupancy", methods=["GET"])
@admin_required
def check_occupancy(unit_code):
    try:
        occupied = is_unit_occupied_by_code(unit_code)

        return jsonify({
            "unit_code": unit_code.upper(),
            "occupied": occupied
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400



@admin_bp.route("/units", methods=["GET"])
@admin_required
def list_all_units():

    units = Unit.query.all()
    today = date.today()
    result = []


    for u in units:
        active_booking = Booking.query.filter(
            Booking.unit_id == u.id,
            Booking.status == "APPROVED",
            Booking.lease_start <= today,
            Booking.lease_end >= today
        ).first()

        result.append({
            "unit_code": u.unit_code,
            "tower_code": u.tower.code,
            "wing": u.wing,
            "floor_number": u.floor_number,
            "flat_number": u.flat_number,
            "rent": str(u.rent),
            "available_from": u.available_from.isoformat(),
            "flat_type": u.flat_type,
            "furnishing": u.furnishing,
            "balcony_type": u.balcony_type,
            "parking": u.parking,
            "facing_direction": u.facing_direction,
            "is_active": u.is_active,
            "occupied": active_booking is not None
        })
    # return jsonify([
    #     {
    #         "unit_code": u.unit_code,
    #         "tower_code": u.tower.code,
    #         "wing": u.wing,
    #         "floor_number": u.floor_number,
    #         "flat_number": u.flat_number,
    #         "rent": str(u.rent),
    #         "available_from": u.available_from.isoformat(),
    #         "flat_type": u.flat_type,
    #         "furnishing": u.furnishing,
    #         "balcony_type": u.balcony_type,
    #         "parking": u.parking,
    #         "facing_direction": u.facing_direction,
    #         "is_active": u.is_active
    #     }
    #     for u in units
    # ]), 200

    return jsonify(result), 200



@admin_bp.route("/units/<string:unit_code>", methods=["GET"])
@admin_required
def get_single_unit(unit_code):

    unit = Unit.query.filter_by(unit_code=unit_code).first_or_404()

    return jsonify({
        "unit_code": unit.unit_code,
        "tower_id": unit.tower_id,
        "wing": unit.wing,
        "floor_number": unit.floor_number,
        "flat_number": unit.flat_number,
        "rent": str(unit.rent),
        "available_from": unit.available_from.isoformat(),
        "flat_type": unit.flat_type,
        "furnishing": unit.furnishing,
        "balcony_type": unit.balcony_type,
        "parking": unit.parking,
        "facing_direction": unit.facing_direction,
        "is_active": unit.is_active
    }), 200
