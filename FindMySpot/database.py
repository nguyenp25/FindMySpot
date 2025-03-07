from pymongo import MongoClient
import bcrypt

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")  # Update as needed
        self.db = self.client['findmyspot_db']
        self.users = self.db['users']

    def add_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users.insert_one({"username": username, "password": hashed_password})

    def get_user(self, username):
        return self.users.find_one({"username": username})
    
    def user_exists(self, username):
        return self.users.find_one({"username": username}) is not None

    def validate_login(self, username, password):
        user_data = self.get_user(username)
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
            return True
        return False
