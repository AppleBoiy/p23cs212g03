import json

def save_user_data(users_data):
    with open('app/data/users.json', 'w') as f:
        json.dump(users_data, f)

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def generate_encrypted_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')