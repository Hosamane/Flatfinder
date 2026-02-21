from app.extensions.db import db
from sqlalchemy.orm import relationship


class Tower(db.Model):
    __tablename__ = "towers"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(50),
        nullable=False
    )

     # Code used for unit naming (K23A)
    code = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )


    locality = db.Column(
        db.String(100),
        index=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    amenities = relationship(
        "Amenity",
        secondary="tower_amenities",
        back_populates="towers"
    )

    units = relationship(
        "Unit",
        back_populates="tower",
        cascade="all, delete-orphan"
    )