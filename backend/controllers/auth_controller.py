from flask import Blueprint, request, jsonify
from services.auth_service import login, signup
from services.token_service import decode_token

auth_router = Blueprint("auth", __name__)

# ==== Register/Signup ==== #
@auth_router.route("/signup", methods=["POST"])
def signup_handler():
    """
    Handle user registration via JSON body.
    """
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password: 
        return jsonify({ "error": "Username and password required" }), 400
    
    try:
        signup(username, password)
        return jsonify({ 
            "message": "Signup Success", 
            "username": username, 
        })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500


# ==== Login (Get Token kub) ==== #
@auth_router.route("/login", methods=["POST"])
def login_handler():
    """
    Handle user login via JSON body.
    Returns a session token on success.
    """
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    token = login(username, password)

    if token:
        return jsonify({
            "message": "Login Success",
            "token": token,
            "username": username,
        })
    else:
        return jsonify({ "error": "Invalid Username or Password" }), 401
    

# ==== User from Token ==== #
@auth_router.route("/profile", methods=["GET"])
def profile_handler():
    """
    Handle user login via JSON body.
    Returns a session token on success.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({ "error": "No token" }), 401
    
    token = auth_header.split(" ")[1]
    try:
        decoded = decode_token(token)
        return jsonify({
            "message": "This is protected data for: ",
            "username": decoded.username
        })
    except:
        return jsonify({ "error": "Invaild token" }), 403