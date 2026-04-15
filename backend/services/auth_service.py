from services import data_service, token_service

def login(username, password):
    """
    Authenticate user and return checked user
    """
    user = data_service.authenticate_user(username, password) 
    return token_service.create_token(user)

def signup(username, password):
    """
    Register a new user in the database.
    """
    data_service.create_user(username, password)