from pymongo import MongoClient
import bcrypt
import datetime
from twilio.rest import Client

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")  # Update as needed
        self.db = self.client['findmyspot_db']
        self.users = self.db['users']
        self.parking_spots = self.db['parking_spots']  # New collection for parking spots

    def add_user(self, username, password, phone=None, initial_balance=0):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {"username": username, "password": hashed_password, "balance": initial_balance}
        if phone:
            user_data["phone"] = phone
        self.users.insert_one(user_data)
        return True  # Indicate successful addition
    
    def change_username_password(self, current_username, new_username, new_password):
        user_data = self.get_user(current_username)

        if user_data:
            # Hash the new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            # Update the username and password
            self.users.update_one(
                {"username": current_username},
                {"$set": {"username": new_username, "password": hashed_password}}
            )
            return True
        else:
            return False

    def get_user(self, username):
        return self.users.find_one({"username": username})
    
    def get_user_balance(self, username):
        user_data = self.get_user(username)
        if user_data:
            return user_data.get('balance', 0)
        return 0    

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
    
    def get_user_reservations(self, username):
        user_reservations = self.parking_spots.find({"reservedBy": username}, {"spotId": 1, "_id": 0})
        return [int(reservation['spotId']) for reservation in user_reservations]


    def reserve_parking_spot(self, username, spot_id):
        # Convert spot_id to integer
        spot_id = int(spot_id)
        if self.parking_spots.find_one({"spotId": spot_id, "isReserved": True}):
            return False  # Spot is already reserved

        self.parking_spots.update_one(
            {"spotId": spot_id}, 
            {"$set": {"isReserved": True, "reservedBy": username, "reservationTime": datetime.datetime.now()}},
            upsert=True
        )

        # Send SMS notification if user has a phone number
        user_data = self.get_user(username)
        if user_data and 'phone' in user_data:
            self.send_sms_notification(user_data['phone'], f"You have successfully reserved parking spot number {spot_id}.")

        return True  # Reservation successful
    
    def unreserve_parking_spot(self, username, spot_id):
        # Convert spot_id to integer
        spot_id = int(spot_id)
        spot = self.parking_spots.find_one({"spotId": spot_id, "reservedBy": username})
        if spot and spot['isReserved']:
            self.parking_spots.update_one({"spotId": spot_id}, {"$set": {"isReserved": False, "reservedBy": None, "reservationTime": None}})

            # Send SMS notification if user has a phone number
            user_data = self.get_user(username)
            if user_data and 'phone' in user_data:
                self.send_sms_notification(user_data['phone'], f"You have successfully unreserved parking spot number {spot_id}.")

            return True  # Unreservation successful
        return False  # Spot not reserved by this user or doesn't exist
    
    def send_sms_notification(self, user_phone, message_body):
        account_sid = 'AC2ea1c971ea162d98295bf49cbb1a984f'
        auth_token = 'a1284fed6431c233d1c0b59849dad731'
        client = Client(account_sid, auth_token)
        twilio_number = '+18667262459'  # Ensure the number is in E.164 format
        try:
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=user_phone
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Failed to send SMS: {e}")

    def update_account_balance(self, username, amount):
        # Fetch the user's current balance
        current_balance = self.users.find_one({"username": username})['balance']
        # Update the balance with the new amount
        new_balance = current_balance + amount
        self.users.update_one({"username": username}, {"$set": {"balance": new_balance}})
        return True  # Indicate successful balance update


    
