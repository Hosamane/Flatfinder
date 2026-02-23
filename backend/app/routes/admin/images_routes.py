# app/routes/admin/image_routes.py

import cloudinary.uploader
from flask import request, jsonify
from app.routes.admin import admin_bp
from app.models.unit import Unit
from app.models.image import Image
from app.extensions.db import db
from app.utils.decorators import admin_required


# @admin_bp.route("/units/<string:unit_code>/upload-image", methods=["POST"])
# @admin_required
# def upload_unit_image(unit_code):

#     unit = Unit.query.filter_by(unit_code=unit_code).first_or_404()

#     if "image" not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files["image"]

#     # Upload to Cloudinary
#     result = cloudinary.uploader.upload(file)

#     # Create Image record
#     image = Image(
#         cloudinary_public_id=result["public_id"],
#         cloudinary_url=result["secure_url"]
#     )

#     db.session.add(image)
#     db.session.flush()   # get image.id before commit

#     # Link image to unit
#     unit.image  = image

#     db.session.commit()

#     return jsonify({
#         "message": "Image uploaded",
#         "image_url": image.cloudinary_url
#     }), 200



@admin_bp.route("/units/<string:unit_code>/upload-image", methods=["POST"])
@admin_required
def upload_unit_image(unit_code):

    unit = Unit.query.filter_by(unit_code=unit_code.upper()).first_or_404()

    if "image" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["image"]

    # 🔥 If image already exists → delete from Cloudinary + DB
    if unit.image:
        cloudinary.uploader.destroy(unit.image.cloudinary_public_id)
        db.session.delete(unit.image)
        db.session.flush()

    # Upload new image
    result = cloudinary.uploader.upload(file)

    # Create new Image record
    image = Image(
        cloudinary_public_id=result["public_id"],
        cloudinary_url=result["secure_url"]
    )

    db.session.add(image)
    db.session.flush()

    # Link image to unit
    unit.image = image

    db.session.commit()

    return jsonify({
        "message": "Image uploaded / replaced successfully",
        "image_url": image.cloudinary_url
    }), 200




@admin_bp.route("/units/<string:unit_code>/delete-image", methods=["DELETE"])
@admin_required
def delete_unit_image(unit_code):

    unit = Unit.query.filter_by(unit_code=unit_code.upper()).first_or_404()

    if not unit.image:
        return jsonify({"error": "No image found"}), 404

    # Delete from Cloudinary
    cloudinary.uploader.destroy(unit.image.cloudinary_public_id)

    # Delete from DB
    db.session.delete(unit.image)
    unit.image = None

    db.session.commit()

    return jsonify({"message": "Image deleted successfully"}), 200