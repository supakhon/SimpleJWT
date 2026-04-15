from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from backend.models.user_model import User


# ===== Database Section ===== #
db = SQLAlchemy()
bcrypt = Bcrypt()

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
    bcrypt.init_app(app)

# ===== Register Section ===== #
def create_user(username, password):
    """
    For Creating User into the database or Add Username and Password into Database

    สร้างผู้ใช้และเอาลง Database หรือการเพิ่มชื่อและรหัสผ่านลงไปใน Database
    """

    # Checking user ซ้ำบ่
    existing_user = User.query.filter_by(username=username).first()
    if existing_user: return None, "User already exists"

    # Hash password
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create Object with a Hash pw
    new_user = User(username=username, password=hashed_pw)

    # Save to DB
    db.session.add(new_user)
    db.session.commit()

    print(f'User {new_user.username} has been created.')
    return new_user, None


# ===== Login Section ===== #
def authenticate_user(username, password):
    """
    Authenticate user from Username and Password

    ฟังก์ชั่นที่เอาไว้ เช็คว่า User คือใคร ผ่าน Username Password
    """
    user = User.query.filter_by(username=username).first()

    if not user: return None, "User not found"
    if not bcrypt.check_password_hash(user.password, password): return None, "Invalid password"

    return user, None


# ===== User Section ===== #
def get_user_by_name(username):
    """
    Fetch user information by Username
    """
    user = User.query.filter_by(username=username).first()

    if not user: return None

    return user

