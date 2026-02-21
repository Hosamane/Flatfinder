
# import os
# from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# # Configure your database URI, e.g., 'postgresql://user:password@host/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# # 'postgresql://flask_user:StrongPassword123!@127.0.0.1/flask_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy()

# @app.route('/healthz')
# def health_check():
#     try:
#         # Try to execute a simple query to check the connection
#         db.session.query(db.func.current_timestamp()).first()
#         return "Database connection successful", 200
#     except Exception as e:
#         # If an exception occurs, the connection has failed
#         return f"Database connection failed: {str(e)}", 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
