from app.extensions.db import db
from sqlalchemy.orm import relationship


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)

    cloudinary_public_id = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    cloudinary_url = db.Column(
        db.String(500),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    units = db.relationship(
        "Unit",
        back_populates="image"
    )
