from app.extensions.db import db
from app.models.booking import Booking
from app.models.unit import Unit
from sqlalchemy import and_


def create_booking(user_id, unit_id, move_in_date):

    unit = Unit.query.get(unit_id)

    if not unit:
        raise ValueError("Unit not found")

    # Step 1: Check if already approved booking exists
    existing_booking = Booking.query.filter(
        Booking.unit_id == unit_id,
        Booking.status == "APPROVED",
        Booking.lease_end == None  # still active
    ).first()

    if existing_booking:
        raise ValueError("Unit already occupied")

    # Step 2: Create pending booking
    booking = Booking(
        user_id=user_id,
        unit_id=unit_id,
        move_in_date=move_in_date,
        rent_snapshot=unit.rent
    )

    db.session.add(booking)
    db.session.commit()

    return booking


def approve_booking(booking_id):

    booking = Booking.query.get(booking_id)

    if not booking:
        raise ValueError("Booking not found")

    if booking.status != "PENDING":
        raise ValueError("Booking already processed")

    # 🔐 TRANSACTION START
    try:

        # Lock the unit row to prevent race condition
        unit = (
            db.session.query(Unit)
            .filter(Unit.id == booking.unit_id)
            .with_for_update()
            .first()
        )

        # Check again inside transaction
        existing_approved = Booking.query.filter(
            Booking.unit_id == booking.unit_id,
            Booking.status == "APPROVED",
            Booking.lease_end == None
        ).first()

        if existing_approved:
            raise ValueError("Unit already occupied")

        booking.status = "APPROVED"
        booking.lease_start = booking.move_in_date

        db.session.commit()

    except:
        db.session.rollback()
        raise

    return booking
