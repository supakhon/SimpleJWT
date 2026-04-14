from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    import os

    db_url = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/dbname')

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1) # 1 meaning first time only na

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url + "?sslmode=require"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)