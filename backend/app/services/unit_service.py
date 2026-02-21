from app.models.unit import Unit
from app.models.tower import Tower
from app.extensions.db import db
from sqlalchemy.orm import joinedload
from datetime import date,datetime
# from datetime import date


def get_filtered_units(filters):

    query = db.session.query(Unit).join(Tower)

    # Only active units
    query = query.filter(Unit.is_active == True)

    # -------- FILTERS -------- #

    if filters.get("flat_type"):
        query = query.filter(Unit.flat_type == filters["flat_type"])

    if filters.get("furnishing"):
        query = query.filter(Unit.furnishing == filters["furnishing"])

    if filters.get("balcony_type"):
        query = query.filter(Unit.balcony_type == filters["balcony_type"])

    if filters.get("parking") is not None:
        query = query.filter(Unit.parking == filters["parking"])

    if filters.get("facing_direction"):
        query = query.filter(
            Unit.facing_direction == filters["facing_direction"]
        )

    if filters.get("locality"):
        query = query.filter(
            Tower.locality == filters["locality"]
        )

    # -------- MOVE-IN DATE LOGIC -------- #

    move_in = filters.get("move_in_date")

    if move_in:
        query = query.filter(Unit.available_from <= move_in)
    else:
        query = query.filter(Unit.available_from <= date.today())

    # -------- SORTING -------- #

    sort = filters.get("sort")

    if sort == "rent_asc":
        query = query.order_by(Unit.rent.asc())

    elif sort == "rent_desc":
        query = query.order_by(Unit.rent.desc())

    elif sort == "availability_asc":
        query = query.order_by(Unit.available_from.asc())

    elif sort == "availability_desc":
        query = query.order_by(Unit.available_from.desc())

    else:
        # Default sort
        query = query.order_by(Unit.created_at.desc())

    return query.options(joinedload(Unit.tower)).all()



def create_unit(tower_code, data):

    tower = Tower.query.filter_by(code=tower_code.upper()).first()

    if not tower:
        raise ValueError("Tower not found")

    wing = data.get("wing")
    flat_number = data.get("flat_number")

    if not wing or not flat_number:
        raise ValueError("Wing and flat number are required")
    unit_code = f"{tower.code}{wing.upper()}{flat_number.upper()}"


    existing_unit = Unit.query.filter_by(unit_code=unit_code).first()
    if existing_unit:
        raise ValueError("Unit with this code already exists")

    floor_number = data.get("floor_number")
    rent = data.get("rent")
    # available_from = data.get("available_from")
    flat_type = data.get("flat_type")
    furnishing = data.get("furnishing")
    balcony_type = data.get("balcony_type")
    parking = data.get("parking")
    facing_direction = data.get("facing_direction")


    available_from = data.get("available_from")

    if available_from:
        available_from = datetime.strptime(
            available_from, "%Y-%m-%d"
        ).date()
    else:
        available_from = date.today()

    unit = Unit(
        tower_id=tower.id,
        unit_code=unit_code.upper(),
        wing=wing,
        floor_number=floor_number,
        flat_number=flat_number,
        rent=rent,
        available_from=available_from,
        flat_type=flat_type,
        furnishing=furnishing,
        balcony_type=balcony_type,
        parking=parking,
        facing_direction=facing_direction
    )

    db.session.add(unit)
    db.session.commit()

    return unit



def get_units_by_tower(tower_code):
    tower = Tower.query.filter_by(code=tower_code.upper()).first()

    if not tower:
        raise ValueError("Tower not found")

    return Unit.query.filter_by(tower_id=tower.id).all()


def delete_unit(unit_code):
    unit = Unit.query.filter_by(unit_code=unit_code.upper()).first()

    if not unit:    
        raise ValueError("Unit not found")
    
    db.session.delete(unit)
    db.session.commit()



def update_unit(unit_code,data):

    unit= Unit.query.filter_by(unit_code=unit_code.upper()).first()

    if not unit:
        raise ValueError("Unit not found")
    
    if "rent" in data:
        unit.rent=data["rent"]

    if "available_from" in data:
        unit.available_from=datetime.strptime(
            data["available_from"], "%Y-%m-%d").date()
    
    if "flat_type" in data:
        unit.flat_type=data["flat_type"]

    if "furnishing" in data:
        unit.furnishing=data["furnishing"]

    if "balcony_type" in data:
        unit.balcony_type=data["balcony_type"]  

    if "parking" in data:
        unit.parking=data["parking"]

    if "facing_direction" in data:  
        unit.facing_direction=data["facing_direction"]

    if "is_active" in data:
        unit.is_active=data["is_active"]
    
    db.session.commit()

    return unit