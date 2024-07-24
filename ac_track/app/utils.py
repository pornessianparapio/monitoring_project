from flask_jwt_extended import get_jwt_identity
from .models import User

def get_current_user():
    user_id = get_jwt_identity()['id']
    return User.query.get(user_id)
