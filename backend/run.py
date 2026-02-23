import os

from app import create_app
from app.utils.create_admin import create_default_admin
from app.extensions import db

app = create_app()
with app.app_context():
    db.create_all() 
    create_default_admin()

    
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5433))
    app.run(host="0.0.0.0", port=port)
