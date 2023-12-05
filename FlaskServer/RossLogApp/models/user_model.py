import datetime

from bson.objectid import ObjectId
from flask_login import UserMixin
# import bcrypt
from passlib.hash import pbkdf2_sha256
from pymongo.errors import PyMongoError

from ..extensions import db

user_collection = db["UserCollection"]

class User(UserMixin):
    def __init__(self, username, passhash, id=""):
        self.id = id
        self.username = username
        self.passhash = passhash # TODO: do we actually ever need to store this?

    def __repr__(self):
        return f'{self.id} - {self.username}'


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
            self.id = user_collection.insert_one(user_data).insertedid
        except PyMongoError as e:
            print(f'ERROR DURING INSERT: {str(e)}')

        return self.id
    

    def getid(self):
        return str(self.id)


    # def update(self):
    #     user_data = {
    #         'username': self.username
    #     }
    #     return user_collection.update_one({'id': ObjectId(self.id)}, {'$set': user_data})


    def delete(self):
        return user_collection.delete_one({'id': ObjectId(self.id)})
    

    @staticmethod
    def to_object(user):
        return User(id=user["_id"], username=user["username"], passhash=user["passhash"])


    @staticmethod
    def get_all():
        return list(user_collection.find())
    

    @staticmethod
    def get_by_id(id: int):
        # return user_collection.find_one({'id': ObjectId(id)})
        return user_collection.find_one({'_id': ObjectId(id)})


    @staticmethod
    def get_by_username(username):
        return user_collection.find_one({'username': username})
    
    
    @staticmethod
    def check_pass(test_username, test_password):
        user = User.get_by_username(test_username)
        print(user)
        if user:
            # return bcrypt.checkpw(test_password.encode('utf-8'), user["passhash"])
            return pbkdf2_sha256.verify(test_password.encode('utf-8'), user["passhash"])
        return False