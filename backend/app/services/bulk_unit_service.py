from datetime import datetime
from app.extensions.db import db
from app.models.unit import Unit
from app.models.tower import Tower


# ----------------------------------------------------
# BULK CREATION USING LIST OF UNITS
# ----------------------------------------------------
def bulk_create_units_list(tower_code, data):

    tower = Tower.query.filter_by(code=tower_code.upper()).first()

    if not tower:
        raise ValueError("Tower not found")

    units_data = data.get("units")

    if not units_data or not isinstance(units_data, list):
        raise ValueError("Units list is required")

    created_units = []

    for item in units_data:

        wing = item.get("wing")
        flat_number = item.get("flat_number")
        rent = item.get("rent")
        available_from = item.get("available_from")

        if not all([wing, flat_number, rent, available_from]):
            continue  # skip incomplete entries

        unit_code = f"{tower.code}{wing.upper()}{flat_number}"

        existing = Unit.query.filter_by(unit_code=unit_code).first()
        if existing:
            continue  # skip duplicates

        unit = Unit(
            tower_id=tower.id,
            wing=wing.upper(),
            flat_number=flat_number,
            floor_number=item.get("floor_number"),
            unit_code=unit_code,
            rent=rent,
            available_from=datetime.strptime(
                available_from, "%Y-%m-%d"
            ).date(),
            flat_type=item.get("flat_type"),
            furnishing=item.get("furnishing"),
            balcony_type=item.get("balcony_type"),
            parking=item.get("parking", False),
            facing_direction=item.get("facing_direction"),
            is_active=item.get("is_active", True),
        )

        db.session.add(unit)
        created_units.append(unit)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return created_units


# ----------------------------------------------------
# BULK CREATION USING RANGE
# ----------------------------------------------------
def bulk_create_by_range(tower_code, data):

    tower = Tower.query.filter_by(code=tower_code.upper()).first()

    if not tower:
        raise ValueError("Tower not found")

    wing = data.get("wing")
    floor_number = data.get("floor_number")
    start_flat = data.get("start_flat")
    end_flat = data.get("end_flat")
    rent = data.get("rent")
    available_from = data.get("available_from")

    if not all([wing, floor_number, start_flat, end_flat, rent, available_from]):
        raise ValueError("Missing required fields")

    available_from = datetime.strptime(
        available_from, "%Y-%m-%d"
    ).date()

    created_units = []

    for flat in range(int(start_flat), int(end_flat) + 1):

        flat_number = str(flat)
        unit_code = f"{tower.code}{wing.upper()}{flat_number}"

        existing = Unit.query.filter_by(unit_code=unit_code).first()
        if existing:
            continue

        unit = Unit(
            tower_id=tower.id,
            wing=wing.upper(),
            flat_number=flat_number,
            floor_number=floor_number,
            unit_code=unit_code,
            rent=rent,
            available_from=available_from,
            flat_type=data.get("flat_type"),
            furnishing=data.get("furnishing"),
            balcony_type=data.get("balcony_type"),
            parking=data.get("parking", False),
            facing_direction=data.get("facing_direction"),
            is_active=data.get("is_active", True),
        )

        db.session.add(unit)
        created_units.append(unit)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return created_units
