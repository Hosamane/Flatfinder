from datetime import date
from sqlalchemy import and_
from app.models.unit import Unit
from app.models.booking import Booking


def is_unit_occupied_by_code(unit_code):

    unit = Unit.query.filter_by(
        unit_code=unit_code.upper()
    ).first()

    if not unit:
        raise ValueError("Unit not found")

    today = date.today()

    active_booking = Booking.query.filter(
        Booking.unit_id == unit.id,
        Booking.status == "APPROVED",
        Booking.lease_start <= today,
        Booking.lease_end >= today
    ).first()

    return active_booking is not None