from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions.db import db
import bcrypt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON body"}), 400

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "Missing fields"}), 400

        # Check existing user
        existing = User.query.filter_by(email=email).first()
        if existing:
            return jsonify({"error": "User already exists"}), 400

        # Hash password
        import bcrypt
        hashed_pw = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            name=name,
            email=email,
            password_hash=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered"}), 201

    except Exception as e:
        print("REGISTER ERROR:", str(e))
        return jsonify({"error": str(e)}), 500




@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        access_token = create_access_token(identity=str(user.id),additional_claims={"role": user.role})



#         return jsonify({
#     "access_token": access_token,
#     "role": user.role
# })

        return jsonify({"message": "Login route reached",
                        "access_token": access_token,
                        "role":user.role}), 200
    
        # # print("Generated access token:", access_token)
        # print("TOKEN:", access_token)
        # return jsonify({"access_token": access_token}), 200

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

from flask_jwt_extended import jwt_required, get_jwt_identity

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"user_id": current_user})
