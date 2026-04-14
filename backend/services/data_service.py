from flask_sqlalchemy import SQLAlchemy


# ===== Database Section ===== #

db = SQLAlchemy()

def init_db(app):
    """
    For Creating Database database.db if it is not exist
    
    ฟังก์ชั่นสำหรับสร้าง Database อย่างไฟล์ database.db ในกรณีที่ไฟล์นี้ไม่มีอยู่
    """

    import os

    db_url = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/dbname')

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1) # 1 meaning first time only na

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url + "?sslmode=require"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)