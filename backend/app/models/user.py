from app.extensions.db import db
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(db.Text, nullable=False)

    role = db.Column(
        db.Enum("USER", "ADMIN", name="user_roles"),
        default="USER",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    bookings = db.relationship(
        "Booking",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    tenant_profile = db.relationship(
        "TenantProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
