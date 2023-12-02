import datetime

from bson.objectid import ObjectId
# import bcrypt
from passlib.hash import pbkdf2_sha256
from pymongo.errors import PyMongoError

from ..extensions import db

user_collection = db["user-collection"]

class User:
    def __init__(self, username, passhash, _id=""):
        self._id = _id
        self.username = username
        self.passhash = passhash


    def debug(self):
        # naughty!  best make sure this doesn't reveal hashes
        print(f'Username: {self.username}')


    def save(self):
        if User.get_by_username(self.username):
            return None
        
        user_data = {
            'username': self.username,
            'passhash': self.passhash
        }

        try:
            self._id = user_collection.insert_one(user_data).inserted_id
        except PyMongoError as e:
            print(f'ERROR DURING INSERT: {str(e)}')

        return self._id
    

    def get_id(self):
        return str(self._id)


    # def update(self):
    #     user_data = {
    #         'username': self.username
    #     }
    #     return user_collection.update_one({'_id': ObjectId(self._id)}, {'$set': user_data})


    def delete(self):
        return user_collection.delete_one({'_id': ObjectId(self._id)})


    @staticmethod
    def get_all():
        return list(user_collection.find())
    

    @staticmethod
    def get_by_id(id):
        return user_collection.find_one({'_id': ObjectId(id)})


    @staticmethod
    def get_by_username(username):
        return user_collection.find_one({'username': username})
    

    @staticmethod
    def get_instance(user_dict):
        this_user = User(
            _id=user_dict["_id"],
            username=user_dict["username"],
            passhash=user_dict["passhash"]
        )
        return this_user
    
    
    @staticmethod
    def check_pass(test_username, test_password):
        user = User.get_by_username(test_username)
        if user:
            # return bcrypt.checkpw(test_password.encode('utf-8'), user["passhash"])
            return pbkdf2_sha256.verify(test_password.encode('utf-8'), user["passhash"])
        return False