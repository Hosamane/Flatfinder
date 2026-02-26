
# from datetime import datetime,date
# from flask import request,jsonify
# from app.routes.public import public_bp
# from app.models.unit import Unit
# from app.services.occupancy_service import is_unit_occupied_by_code

# @public_bp.route("/towers/<string:code>/units", methods=["GET"])
# def get_available_units(code):

#     move_in_date = request.args.get("move_in_date")


#     if move_in_date:
#         move_in_date = datetime.strptime(move_in_date, "%Y-%m-%d").date()
#     else:
#         move_in_date = date.today()


#     units = Unit.query.join(Unit.tower).filter(
#         Unit.is_active == True,
#         Unit.available_from <= move_in_date
#     ).all()


#     units = [u for u in units if u.tower.code == code.upper()]

#     available_units = [
#         u for u in units
#         if not is_unit_occupied_by_code(u.unit_code)
#     ]

#     return jsonify ([
#         {
#             "unit_code":u.unit_code,
#             "rent":str(u.rent),
#             "flat_type":u.flat_type,
#             "furnishing":u.furnishing,
#             "balcony_type":u.balcony_type,
#             "parking":u.parking, 
#             "facing_direction":u.facing_direction,
#             "available_from":u.available_from.isoformat()

#         }
#         for u in available_units
#     ])


from datetime import datetime, date
from flask import request, jsonify
from sqlalchemy import and_, or_
from app.routes.public import public_bp
from app.models.unit import Unit
from app.models.tower import Tower
from app.models.booking import Booking


@public_bp.route("/towers/<string:code>/units", methods=["GET"])
def get_available_units(code):

    move_in_date = request.args.get("move_in_date")

    if move_in_date:
        move_in_date = datetime.strptime(move_in_date, "%Y-%m-%d").date()
    else:
        move_in_date = date.today()
    
    #before lease    
    # beforeLease = (
    #     Booking.query.filter(
    #         Booking.exitedBeforeLeaseEnd == True
    #     )
    #     .with_entities(Booking.unit_id)
    #     .subquery()
    # )


    # Subquery to find occupied unit IDs
    occupied_subquery = (
        Booking.query
        .filter(
            Booking.status == "APPROVED",
            Booking.lease_start <= move_in_date,
            Booking.lease_end >= move_in_date
        )
        .with_entities(Booking.unit_id)
        .subquery()
    )

    # Main query
    units = (
        Unit.query
        .join(Tower)
        .filter(
            Tower.code == code.upper(),
            Unit.is_active == True,
            Unit.available_from <= move_in_date,
            ~Unit.id.in_(occupied_subquery),
            
        )
        .all()
    )

    return jsonify([
        {
            "image_url": u.image.cloudinary_url if u.image else None,
            "unit_code": u.unit_code,
            "rent": str(u.rent),
            "flat_type": u.flat_type,
            "furnishing": u.furnishing,
            "balcony_type": u.balcony_type,
            "parking": u.parking,
            "facing_direction": u.facing_direction,
            "available_from": u.available_from.isoformat(),
             "image_url": u.image.cloudinary_url if u.image else None
        }
        for u in units
    ])


@public_bp.route("/units/<string:unit_code>", methods=["GET"])
def get_unit_by_code(unit_code):

    unit = (
        Unit.query
        .join(Tower)
        .filter(Unit.unit_code == unit_code.upper())
        .first()
    )

    if not unit:
        return jsonify({"error": "Unit not found"}), 404

    # Check occupancy
    today = date.today()

    occupied = Booking.query.filter(
        Booking.unit_id == unit.id,
        Booking.status == "APPROVED",
        Booking.lease_start <= today,
        Booking.lease_end >= today
    ).first() is not None

    return jsonify({
        "unit_code": unit.unit_code,
        "rent": str(unit.rent),
        "flat_type": unit.flat_type,
        "furnishing": unit.furnishing,
        "balcony_type": unit.balcony_type,
        "parking": unit.parking,
        "facing_direction": unit.facing_direction,
        "available_from": unit.available_from.isoformat(),
        "occupied": occupied,
        "image_url": unit.image.cloudinary_url if unit.image else None,
        "tower": {
            "name": unit.tower.name,
            "code": unit.tower.code
        }
    })


@public_bp.route("/units/<string:unit_code>", methods=["GET"])
def get_unit_detail(unit_code):

    unit = Unit.query.filter_by(unit_code=unit_code).first_or_404()

    return jsonify({
        "unit_code": unit.unit_code,
        "rent": str(unit.rent),
        "flat_type": unit.flat_type,
        "furnishing": unit.furnishing,
        "balcony_type": unit.balcony_type,
        "parking": unit.parking,
        "facing_direction": unit.facing_direction,
        "available_from": unit.available_from.isoformat(),
        "image_url": unit.image.cloudinary_url if unit.image else None
    })
