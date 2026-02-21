from app.models.unit import Unit
from app.models.booking import Booking
from app.extensions.db import db
from sqlalchemy import func


def get_dashboard_stats():

    # Total Units
    total_units = db.session.query(func.count(Unit.id)).scalar()

    # Occupied Units
    occupied_units = (
        db.session.query(func.count(Booking.id))
        .filter(
            Booking.status == "APPROVED",
            Booking.lease_end == None
        )
        .scalar()
    )

    # Available Units
    available_units = total_units - occupied_units

    # Pending Bookings
    pending_bookings = (
        db.session.query(func.count(Booking.id))
        .filter(Booking.status == "PENDING")
        .scalar()
    )

    # Occupancy %
    occupancy_percentage = 0

    if total_units > 0:
        occupancy_percentage = round(
            (occupied_units / total_units) * 100, 2
        )

    return {
        "total_units": total_units,
        "occupied_units": occupied_units,
        "available_units": available_units,
        "pending_bookings": pending_bookings,
        "occupancy_percentage": occupancy_percentage
    }
