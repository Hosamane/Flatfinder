# from flask import jsonify
# from datetime import date, timedelta
# from sqlalchemy import func
# from app.extensions import db
# from app.routes.admin import admin_bp
# from app.models.unit import Unit
# from app.models.tower import Tower
# from app.models.booking import Booking
# from app.utils.decorators import admin_required
# from app import db

# @admin_bp.route("/dashboard", methods=["GET"])
# @admin_required
# def admin_dashboard():

#     today = date.today()
#     first_day_month = today.replace(day=1)

#     # 🔹 Totals
#     total_towers = Tower.query.count()
#     total_units = Unit.query.count()

#     occupied_units = Booking.query.filter(
#         Booking.status == "APPROVED",
#         Booking.lease_start <= today,
#         Booking.lease_end >= today
#     ).count()

#     available_units = total_units - occupied_units

#     active_bookings = Booking.query.filter(
#         Booking.status == "APPROVED",
#         Booking.lease_end >= today
#     ).count()

#     # 🔹 Revenue This Month
#     revenue_this_month = db.session.query(
#         func.sum(Unit.rent)
#     ).join(Booking, Booking.unit_id == Unit.id).filter(
#         Booking.status == "APPROVED",
#         Booking.lease_start >= first_day_month
#     ).scalar() or 0

#     # 🔹 Recent Bookings
#     recent_bookings = Booking.query.order_by(
#         Booking.created_at.desc()
#     ).limit(5).all()

#     recent_data = [{
#         # "tenant": b.tenant_name,
#         "unit_code": b.unit.unit_code,
#         "start": b.lease_start,
#         "status": b.status
#     } for b in recent_bookings]

#     # 🔹 Lease Expiry (Next 30 Days)
#     expiry_date = today + timedelta(days=30)

#     expiring = Booking.query.filter(
#         Booking.status == "APPROVED",
#         Booking.lease_end.between(today, expiry_date)
#     ).all()

#     expiry_data = [{
#         # "tenant": b.tenant_name,
#         "unit_code": b.unit.unit_code,
#         "lease_end": b.lease_end
#     } for b in expiring]

#     return jsonify({
#         "total_towers": total_towers,
#         "total_units": total_units,
#         "occupied_units": occupied_units,
#         "available_units": available_units,
#         "active_bookings": active_bookings,
#         "revenue_this_month": revenue_this_month,
#         "recent_bookings": recent_data,
#         "lease_expiry": expiry_data
#     })













from flask import jsonify
from datetime import date, timedelta
from sqlalchemy import func
from app.routes.admin import admin_bp
from app.models import Unit, Tower, Booking
from app.extensions.db import db
from app.utils.decorators import admin_required


@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def admin_dashboard():

    today = date.today()
    first_day_month = today.replace(day=1)

    total_towers = Tower.query.count()
    total_units = Unit.query.count()

    occupied_units = Booking.query.filter(
        Booking.status == "APPROVED",
        Booking.lease_start <= today,
        Booking.lease_end >= today
    ).count()

    available_units = total_units - occupied_units

    active_bookings = Booking.query.filter(
        Booking.status == "APPROVED",
        Booking.lease_end >= today
    ).count()

    # Revenue (Sum of Unit rent for approved bookings this month)
    revenue_this_month = db.session.query(
        func.sum(Unit.rent)
    ).join(Booking, Booking.unit_id == Unit.id).filter(
        Booking.status == "APPROVED",
        Booking.lease_start >= first_day_month
    ).scalar() or 0

    # Recent bookings
    recent = Booking.query.order_by(
        Booking.created_at.desc()
    ).limit(5).all()

    recent_data = [{
        "tenant": b.user.name,
        "unit_code": b.unit.unit_code,
        "start": b.lease_start,
        "status": b.status
    } for b in recent]

    # Lease expiry in next 30 days
    expiry_limit = today + timedelta(days=30)

    expiring = Booking.query.filter(
        Booking.status == "APPROVED",
        Booking.lease_end.between(today, expiry_limit)
    ).all()

    expiry_data = [{
        "tenant": b.user.name,
        "unit_code": b.unit.unit_code,
        "lease_end": b.lease_end
    } for b in expiring]

    return jsonify({
        "total_towers": total_towers,
        "total_units": total_units,
        "occupied_units": occupied_units,
        "available_units": available_units,
        "active_bookings": active_bookings,
        "revenue_this_month": revenue_this_month,
        "recent_bookings": recent_data,
        "lease_expiry": expiry_data
    })