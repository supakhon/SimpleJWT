import jwt
import datetime
import os

SECRET = os.environ.get("SECRET")

def create_token(user):
    token = jwt.encode({
        "id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    }, SECRET, algorithm="HS256")

    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token