from pymongo import MongoClient
import bcrypt
import datetime

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")  # Update as needed
        self.database = self.client['findMySpotDataBase']
        self.users = self.database['users']
        self.parking_spots = self.db['parkingSpots']  # New collection for parking spots

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

    def get_all_reserved_spots(self):
        reserved_spots = self.parking_spots.find({"isReserved": True}, {"spotId": 1, "_id": 0})
        return [spot['spotId'] for spot in reserved_spots]

    def reserve_parking_spot(self, username, spot_id):
        # Convert spot_id to integer
        spot_id = int(spot_id)
        if self.parking_spots.find_one({"spotId": spot_id, "isReserved": True}):
            return False  # Spot is already reserved
        self.parking_spots.update_one({"spotId": spot_id}, {"$set": {"isReserved": True, "reservedBy": username, "reservationTime": datetime.datetime.now()}}, upsert=True)
        return True  # Reservation successful
    
    def unreserve_parking_spot(self, username, spot_id):
        # Convert spot_id to integer
        spot_id = int(spot_id)
        spot = self.parking_spots.find_one({"spotId": spot_id, "reservedBy": username})
        if spot and spot['isReserved']:
            self.parking_spots.update_one({"spotId": spot_id}, {"$set": {"isReserved": False, "reservedBy": None, "reservationTime": None}})
            return True  # Unreservation successful
        return False  # Spot not reserved by this user or doesn't exist