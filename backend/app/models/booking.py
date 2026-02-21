from app.extensions.db import db
from sqlalchemy.orm import relationship


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey("units.id"),
        nullable=False,
        index=True
    )

    status = db.Column(
        db.Enum("PENDING", "APPROVED", "REJECTED", name="booking_status"),
        default="PENDING",
        nullable=False,
        index=True
    )

    move_in_date = db.Column(db.Date, nullable=False)

    lease_start = db.Column(db.Date)
    lease_end = db.Column(db.Date)

    rent_snapshot = db.Column(db.Numeric(10, 2))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship("User", back_populates="bookings")
    unit = db.relationship("Unit", back_populates="bookings")
