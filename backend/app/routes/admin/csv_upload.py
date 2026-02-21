from flask import Blueprint, request, jsonify
from app.models.unit import Unit
from app.models.tower import Tower
from app.extensions.db import db
import csv
import io
from datetime import datetime
from app.utils.decorators import admin_required
from app.routes.admin import admin_bp


# @admin_bp.route("/csv-upload", methods=["POST"])
# @admin_required
# def bulk_upload_units():

#     # 1️⃣ Check file
#     if "admin_csv" not in request.files:
#         return jsonify({"error": "admin_csv file required"}), 400

#     file = request.files["admin_csv"]

#     # 2️⃣ Read CSV
#     stream = io.StringIO(file.stream.read().decode("UTF8"))
#     csv_reader = csv.DictReader(stream)

#     created = 0
#     skipped = 0
#     errors = []

#     # 3️⃣ Loop through rows
#     for row in csv_reader:
#         try:
#             # Skip duplicate unit_code
#             if Unit.query.filter_by(unit_code=row["unit_code"]).first():
#                 skipped += 1
#                 continue

#             # Create unit
#             unit = Unit(
#                 tower_id=int(row["tower_id"]),
#                 unit_code=row["unit_code"],
#                 wing=row["wing"],
#                 floor_number=int(row["floor_number"]),
#                 flat_number=row["flat_number"],
#                 rent=row["rent"],
#                 available_from=datetime.strptime(
#                     row["available_from"], "%Y-%m-%d"
#                 ).date(),
#                 flat_type=row["flat_type"],
#                 furnishing=row["furnishing"],
#                 balcony_type=row["balcony_type"],
#                 parking=row["parking"].lower() == "true",
#                 facing_direction=row["facing_direction"],
#                 is_active=True
#             )

#             db.session.add(unit)
#             created += 1

#         except Exception as e:
#             errors.append({
#                 "unit_code": row.get("unit_code"),
#                 "error": str(e)
#             })

#     # 4️⃣ Commit once at end
#     db.session.commit()

#     return jsonify({
#         "created": created,
#         "skipped_existing": skipped,
#         "errors": errors
#     }), 200









# @admin_bp.route("/csv-upload", methods=["POST"])
# @admin_required
# def bulk_upload_units():

#     if "admin_csv" not in request.files:
#         return jsonify({"error": "admin_csv file required"}), 400

#     file = request.files["admin_csv"]

#     stream = io.StringIO(file.stream.read().decode("UTF8"))
#     csv_reader = csv.DictReader(stream)

#     created = 0
#     skipped = 0
#     errors = []

#     for row in csv_reader:
#         try:
#             # 🔥 Get tower using tower_code
#             tower = Tower.query.filter_by(
#                 code=row["tower_code"].strip().upper()
#             ).first()

#             if not tower:
#                 errors.append({
#                     "unit_code": row.get("unit_code"),
#                     "error": f"Tower code {row.get('tower_code')} not found"
#                 })
#                 continue

#             # Skip duplicate unit_code
#             if Unit.query.filter_by(unit_code=row["unit_code"]).first():
#                 skipped += 1
#                 continue

#             unit = Unit(
#                 tower_id=tower.id,  # 🔥 derived from code
#                 unit_code=row["unit_code"].strip(),
#                 wing=row["wing"].strip(),
#                 floor_number=int(row["floor_number"]),
#                 flat_number=row["flat_number"].strip(),
#                 rent=row["rent"],
#                 available_from=datetime.strptime(
#                     row["available_from"], "%Y-%m-%d"
#                 ).date(),
#                 flat_type=row["flat_type"].strip(),
#                 furnishing=row["furnishing"].strip(),
#                 balcony_type=row["balcony_type"].strip(),
#                 parking=row["parking"].strip().lower() == "true",
#                 facing_direction=row["facing_direction"].strip(),
#                 is_active=True
#             )

#             db.session.add(unit)
#             created += 1

#         except Exception as e:
#             errors.append({
#                 "unit_code": row.get("unit_code"),
#                 "error": str(e)
#             })

#     db.session.commit()

#     return jsonify({
#         "created": created,
#         "skipped_existing": skipped,
#         "errors": errors
#     }), 200











@admin_bp.route("/csv-upload", methods=["POST"])
@admin_required
def bulk_upload_units():

    if "admin_csv" not in request.files:
        return jsonify({"error": "admin_csv file required"}), 400

    file = request.files["admin_csv"]
    stream = io.StringIO(file.stream.read().decode("UTF8"))
    csv_reader = csv.DictReader(stream)

    created = 0
    skipped = 0
    errors = []

    for row in csv_reader:
        try:
            tower = Tower.query.filter_by(
                code=row["tower_code"].strip().upper()
            ).first()

            if not tower:
                errors.append({
                    "error": f"Tower code {row.get('tower_code')} not found"
                })
                continue

            wing = row["wing"].strip().upper()
            flat_number = row["flat_number"].strip()

            # 🔥 Auto generate unit_code
            generated_unit_code = f"{tower.code}{wing}{flat_number}"

            # Check duplicate
            if Unit.query.filter_by(unit_code=generated_unit_code).first():
                skipped += 1
                continue

            unit = Unit(
                tower_id=tower.id,
                unit_code=generated_unit_code,  # 🔥 generated here
                wing=wing,
                floor_number=int(row["floor_number"]),
                flat_number=flat_number,
                rent=row["rent"],
                available_from=datetime.strptime(
                    row["available_from"], "%Y-%m-%d"
                ).date(),
                flat_type=row["flat_type"].strip(),
                furnishing=row["furnishing"].strip(),
                balcony_type=row["balcony_type"].strip(),
                parking=row["parking"].strip().lower() == "true",
                facing_direction=row["facing_direction"].strip(),
                image_id=int(row["image_id"]) if row.get("image_id") else None,
                is_active=True
            )

            db.session.add(unit)
            created += 1

        except Exception as e:
            errors.append({
                "error": str(e)
            })

    db.session.commit()

    return jsonify({
        "created": created,
        "skipped_existing": skipped,
        "errors": errors
    }), 200