# app/routes/admin/image_routes.py

import cloudinary.uploader
from flask import request, jsonify
from app.routes.admin import admin_bp
from app.models.unit import Unit
from app.models.image import Image
from app.extensions.db import db
from app.utils.decorators import admin_required


@admin_bp.route("/units/<string:unit_code>/upload-image", methods=["POST"])
@admin_required
def upload_unit_image(unit_code):

    unit = Unit.query.filter_by(unit_code=unit_code).first_or_404()

    if "image" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["image"]

    # Upload to Cloudinary
    result = cloudinary.uploader.upload(file)

    # Create Image record
    image = Image(
        cloudinary_public_id=result["public_id"],
        cloudinary_url=result["secure_url"]
    )

    db.session.add(image)
    db.session.flush()   # get image.id before commit

    # Link image to unit
    unit.image  = image

    db.session.commit()

    return jsonify({
        "message": "Image uploaded",
        "image_url": image.cloudinary_url
    }), 200
