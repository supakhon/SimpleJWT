from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import jwt
import datetime
import os
import uuid

app = Flask(__name__, static_folder='public')
bcrypt = Bcrypt(app)

# ----- Database ----- #
db_url = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
# db_url = 'sqlite:///test.db'

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Table Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create Table (First time only)
with app.app_context():
    db.create_all()

SECRET = os.environ.get('SECRET', 'mysecretkey') # Get it From Env (Environment)

# Register
@app.post('/register')
def register():
    data = request.json
    name = data.get('name')
    password = data.get('password')

    if User.query.filter_by(name=name).first():
        return jsonify({ "error": "User already exists" }), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({ "id": new_user.id, "name": name }), 201

# Login
@app.post('/login')
def login():
    data = request.json
    user = User.query.filter_by(name=data.get('name')).first()

    if user and bcrypt.check_password_hash(user.password, data.get('password')):
        token = jwt.encode({
            'id': user.id,
            'name': user.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
        }, SECRET, algorithm="HS256")
        return jsonify({ 'token': token })
    return jsonify({"error": "Unauthorized"}), 401

# Route for (HTML/CSS/JS in public folder)
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.get('/profile')
def profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({ "error": "No token" }), 401
    
    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return jsonify({
            "message": "This is protected data",
            "user": decoded
        })
    except:
        return jsonify({ "error": "Invalid token" }), 403

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)), debug = True)