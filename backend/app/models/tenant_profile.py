from app.extensions.db import db
from sqlalchemy.orm import validates, relationship
import re


class TenantProfile(db.Model):
    __tablename__ = "tenant_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    tenant_type = db.Column(
        db.Enum("STUDENT", "WORKING", name="tenant_types"),
        nullable=False
    )

    date_of_birth = db.Column(db.Date, nullable=False)

    college_name = db.Column(db.String(150))
    department = db.Column(db.String(100))

    company_name = db.Column(db.String(150))
    designation = db.Column(db.String(100))

    id_proof_type = db.Column(
        db.Enum("PAN", "AADHAAR", name="id_proof_types"),
        nullable=False
    )

    id_proof_number = db.Column(db.String(20), nullable=False)

    user = db.relationship("User", back_populates="tenant_profile")

    @validates("id_proof_number")
    def validate_id_proof(self, key, value):

        if self.id_proof_type == "PAN":
            pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"
            if not re.match(pattern, value):
                raise ValueError("Invalid PAN format.")

        elif self.id_proof_type == "AADHAAR":
            pattern = r"^[0-9]{12}$"
            if not re.match(pattern, value):
                raise ValueError("Aadhaar must be 12 digits.")

        return value
