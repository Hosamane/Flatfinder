from app import db
from app.models import User
# from werkzeug.security import generate_password_hash
import os
import bcrypt

def create_default_admin():
    admin_email = os.getenv("ADMIN_EMAIL")
    # "admin@rental.com"
    admin_password = os.getenv("ADMIN_PASSWORD") 
    # "admin123"

    admin = User.query.filter_by(email=admin_email).first()
    hashed_pw = bcrypt.hashpw(admin_password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
    if not admin:
        admin = User(
            name="Admin",
            email=admin_email,
            password_hash=hashed_pw,
            role="ADMIN"
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Default admin created")
    else:
        print("ℹ️ Admin already exists")
