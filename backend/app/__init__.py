import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import db, jwt, migrate
from app.routes import register_blueprints
from flask_cors import CORS
import cloudinary
load_dotenv()


def create_app():
    app = Flask(__name__)
    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("CLOUD_API_KEY"),
        api_secret=os.getenv("CLOUD_API_SECRET"),
        secure=True
    )
    # print("Cloud Name:", os.getenv("CLOUD_NAME"))

    # print("DATABASE_URL:", os.getenv("DATABASE_URL"))

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        CORS(app, origins=["http://localhost:8080","http://localhost:4200"])
    # else:
    #     CORS(app)  



    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("Database URL not set")
    
    #railway fix
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://","postgresql://",1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # 👇 IMPORTANT: import models AFTER db init
    with app.app_context():
        from app import models


    register_blueprints(app)

    return app
