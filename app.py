from flask import Flask
from flask_cors import CORS
import os

from backend.models.user_model import User # Need to let SQLAlchemy see Model to use 
from backend.services.data_service import init_db, db

app = Flask(__name__, static_folder='frontend', template_folder='frontend/routes',)

CORS(app)

init_db(app)

with app.app_context(): # Create Table (First time only)
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = int(os.environ.get("PORT", 3000)), debug = os.environ.get("ENV") != "production")