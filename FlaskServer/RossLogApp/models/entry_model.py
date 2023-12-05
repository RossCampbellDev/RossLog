import datetime

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from ..extensions import db

entry_collection = db["EntryCollection"]

class Entry():
    def __init__(self, id, datestamp, title="No Title", body="No Body", tags=""):
        self.id = id
        self.title = title
        self.body = body
        self.tags = tags
        self.datestamp = datetime.now() if datestamp is None else datestamp

    def __repr__(self):
        return f'{self.datestamp} {self.title} - {self.body}'


    def debug(self):
        # naughty!  best make sure this doesn't reveal hashes
        print(f'entryname: {self.entryname}')


    def save(self):
        if Entry.to_object(Entry.get_by_id(self.id)):
            return None
        
        entry_data = {
            'title': self.title,
            'body': self.body,
            'tags': self.tags,
            'datestamp': datetime.now() if self.datestamp is None else self.datestamp
        }

        try:
            self.id = entry_collection.insert_one(entry_data).insertedid
        except PyMongoError as e:
            print(f'ERROR DURING INSERT: {str(e)}')

        return self.id
    

    def getid(self):
        return str(self.id)


    # def update(self):
    #     entry_data = {
    #         'entryname': self.entryname
    #     }
    #     return entry_collection.update_one({'id': ObjectId(self.id)}, {'$set': entry_data})


    def delete(self):
        return entry_collection.delete_one({'_id': ObjectId(self.id)})
    

    @staticmethod
    def to_object(entry):
        return Entry(id=entry["_id"], title=entry["title"], body=entry["body"], tags=entry["tags"], datestamp=entry["datestamp"])
    

    @staticmethod
    def get_all():
        return list(entry_collection.find().sort('datestam', -1))   # descending datestamp order
    

    @staticmethod
    def get_by_id(id: int):
        # return entry_collection.find_one({'id': ObjectId(id)})
        return entry_collection.find_one({'_id': ObjectId(id)})


    @staticmethod
    def get_by_entryname(entryname: str):
        return entry_collection.find_one({'entryname': entryname})