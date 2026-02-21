# from app.extensions.db import db
# from sqlalchemy.orm import relationship


# tower_amenities = db.Table(
#     "tower_amenities",
#     db.Column("tower_id", db.Integer, db.ForeignKey("towers.id"), primary_key=True),
#     db.Column("amenity_id", db.Integer, db.ForeignKey("amenities.id"), primary_key=True),
# )


# class Amenity(db.Model):
#     __tablename__ = "amenities"

#     id = db.Column(db.Integer, primary_key=True)

#     name = db.Column(
#         db.String(50),
#         unique=True,
#         nullable=False
#     )

#     towers = db.relationship(
#         "Tower",
#         secondary=tower_amenities,
#         backref="amenities"
#     )
from app.extensions.db import db
from sqlalchemy.orm import relationship


tower_amenities = db.Table(
    "tower_amenities",
    db.Column("tower_id", db.Integer, db.ForeignKey("towers.id"), primary_key=True),
    db.Column("amenity_id", db.Integer, db.ForeignKey("amenities.id"), primary_key=True),
)


class Amenity(db.Model):
    __tablename__ = "amenities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    towers = relationship(
        "Tower",
        secondary=tower_amenities,
        back_populates="amenities"
    )
