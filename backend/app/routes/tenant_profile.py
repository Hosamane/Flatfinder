
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import TenantProfile

from app.extensions import db
from app.extensions.jwt import jwt
tenant_bp = Blueprint("tenant_profiles", __name__)

# @tenant_bp.route("/tenant-profile", methods=["GET"])
# @jwt_required()
# def get_profile():

#     user_id = get_jwt_identity()

#     profile = TenantProfile.query.filter_by(user_id=user_id).first()

#     if not profile:
#         return jsonify({}), 404

#     return jsonify({
#         "tenant_type": profile.tenant_type,
#         "date_of_birth": profile.date_of_birth,
#         "college_name": profile.college_name,
#         "company_name": profile.company_name,
#         "designation": profile.designation,
#         "id_proof_type": profile.id_proof_type,
#         "id_proof_number": profile.id_proof_number
#     })


@tenant_bp.route("/tenant-profile", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()
    profile = TenantProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({
            "profile_exists": False
        }), 200   # 🔥 NOT 404

    return jsonify({
        "profile_exists": True,
        "tenant_type": profile.tenant_type,
        "date_of_birth": str(profile.date_of_birth),
        "college_name": profile.college_name,
        "department": profile.department,
        "company_name": profile.company_name,
        "designation": profile.designation,
        "id_proof_type": profile.id_proof_type,
        "id_proof_number": profile.id_proof_number
    })

@tenant_bp.route("/tenant-profile", methods=["PUT"])
@jwt_required()
def create_or_update_profile():

    user_id = get_jwt_identity()
    data = request.json

    profile = TenantProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        profile = TenantProfile(user_id=user_id)

    profile.tenant_type = data["tenant_type"]
    profile.date_of_birth = data["date_of_birth"]
    profile.college_name = data.get("college_name")
    profile.department = data.get("department")
    profile.company_name = data.get("company_name")
    profile.designation = data.get("designation")
    profile.id_proof_type = data["id_proof_type"]
    profile.id_proof_number = data["id_proof_number"]

    db.session.add(profile)
    db.session.commit()

    # 🔥 Return updated profile immediately
    return jsonify({
        "tenant_type": profile.tenant_type,
        "date_of_birth": profile.date_of_birth,
        "college_name": profile.college_name,
        "company_name": profile.company_name,
        "designation": profile.designation,
        "id_proof_type": profile.id_proof_type,
        "id_proof_number": profile.id_proof_number
    })