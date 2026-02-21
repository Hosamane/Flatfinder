from app.extensions.db import db
from sqlalchemy import (
    String, Integer, Float, Boolean, Date, DateTime, ForeignKey,
    func, Index, UniqueConstraint, Table
)
from sqlalchemy.orm import relationship


class Unit(db.Model):
    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True)

    tower_id = db.Column(
        db.Integer,
        db.ForeignKey("towers.id", ondelete="CASCADE"),
        nullable=False
    )

    tower = db.relationship("Tower", back_populates="units")

    # Example: K23A102
    unit_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )
    wing = db.Column(db.String(5), nullable=False)
    floor_number = db.Column(db.Integer, nullable=False)
    flat_number = db.Column(db.String(10), nullable=False)

    rent = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        index=True
    )

    available_from = db.Column(
        db.Date,
        nullable=False,
        index=True
    )

    flat_type = db.Column(
        db.Enum("1BHK", "2BHK", "3BHK", name="flat_types"),
        nullable=False,
        index=True
    )

    furnishing = db.Column(
        db.Enum(
            "Fully Furnished",
            "Fully Furnished AC",
            "Semi-Furnished",
            name="furnishing_types"
        ),
        nullable=False,
        index=True
    )

    balcony_type = db.Column(
        db.Enum("Road Facing Balcony",
                "Without Road Facing Balcony",
                "Double Balcony Road facing",
                "Triple Balcony No Road",
                "Triple Balcony Road facing",
                "Without Balcony",
                "Without Road Facing Double Balcony",
                "Double Balcony", 
                name="balcony_type"), index=True)

    parking = db.Column(
        db.Boolean,
        default=False,
        index=True
    )

    facing_direction = db.Column(
        db.Enum(
            "East", "West", "North", "South",
            "North-East", "North-West",
            "South-East", "South-West",
            name="facing_directions"
        )
    )

    image_id = db.Column(
        db.Integer,
        db.ForeignKey("images.id")
    )

    image = db.relationship("Image", back_populates="units")

    is_active = db.Column(
        db.Boolean,
        default=True,
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    bookings = db.relationship(
        "Booking",
        back_populates="unit",
        cascade="all, delete-orphan"
    )


table_args__ = (
        Index("idx_unit_search", "flat_type", "furnishing", "rent", "available_from"),
    )