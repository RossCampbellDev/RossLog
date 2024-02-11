from datetime import datetime

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from datetime import datetime

from ..extensions import db

entry_collection = db["EntryCollection"]

class Entry():
	def __init__(self, id=None, datestamp=datetime.now() , title="No Title", body="No Body", tags=""):
		self.id = id
		self.title = title
		self.body = body
		self.tags = tags
		self.datestamp = datestamp

	def __repr__(self):
		return f'{self.datestamp} {self.title} - {self.body}'


	def debug(self):
		# naughty!  best make sure this doesn't reveal hashes
		print(f'entryname: {self.entryname}')


	def save(self):
		entry_data = {
			'title': self.title,
			'body': self.body,
			'tags': self.tags,
			'datestamp': self.datestamp # datetime.now().strftime("%Y-%m-%d %H:%M") if self.datestamp is None else 
		}

		try:
			self.id = entry_collection.insert_one(entry_data)
		except PyMongoError as e:
			print(f'ERROR DURING INSERT: {str(e)}')

		return self.id
	

	def getid(self):
		return str(self.id)


	def delete(self):
		return entry_collection.delete_one({'_id': ObjectId(self.id)})
	

	def save_to_db(self) -> str:	# do validation at front end
		return entry_collection.insert_one(self)


	def update(self, id):
		entry_data = {
			'title': self.title,
			'body': self.body,
			'tags': self.tags
		}
		print(entry_data)
		return entry_collection.update_one({'_id': ObjectId(id)}, {'$set': entry_data})
	

	@staticmethod
	def get_all():
		return list(entry_collection.find().sort('datestamp', -1))


	@staticmethod
	def get_by_date(search_date: datetime):
		return list(entry_collection.find({
		'date_field': {
			'$gte': datetime.combine(search_date, datetime.min.time()),
			'$lt': datetime.combine(search_date, datetime.max.time())
		}
		}).sort('datestamp', -1))


	@staticmethod
	def get_from_date(start_date: datetime):
		return list(entry_collection.find({
			'datestamp': {
				'$gte': start_date
			}
		}).sort('datestamp', -1))


	@staticmethod
	def get_between_date(start_date: datetime, end_date: datetime) -> list:
		return list(entry_collection.find({
			'datestamp': {
				'$gte': start_date,
				'$lte': end_date
			}
		}).sort('datestamp', -1))
	

	@staticmethod
	def get_by_tags(tags: list) -> list:
		return list(entry_collection.find({
			'tags': {
				'$elemMatch': {
					'$in': tags
				}
			}
		}).sort('datestamp', -1))
	

	@staticmethod
	def get_by_title(title: list) -> list:
		return list(entry_collection.find({
			'title': {
				'$regex': title, '$options': 'i'
			}
		}).sort('datestamp', -1))
	

	@staticmethod
	def get_by_body(body: list) -> list:
		return list(entry_collection.find({
			'body': {
				'$regex': body, '$options': 'i'
			}
		}).sort('datestamp', -1))
	

	@staticmethod
	def get_by_id(id: str):
		# return entry_collection.find_one({'id': ObjectId(id)})
		return entry_collection.find_one({'_id': ObjectId(id)})


	@staticmethod
	def get_by_entryname(entryname: str):
		return entry_collection.find_one({'entryname': entryname})
	
	
	@staticmethod
	def get_by_criteria(criteria: dict=None):
		return list(entry_collection.find(criteria).sort('datestamp', -1)) if criteria else None
	

	@staticmethod
	def get_by_month(criteria: str):
		year = int(criteria.split('-')[0])
		month = int(criteria.split('-')[1])
		date_start = datetime(year, month, 1)
		date_end = datetime(year, month+1, 1) if month < 12 else datetime(year+1, 1, 1)

		return list(entry_collection.find({
			'datestamp': {
				'$gte': date_start,
				'$lte': date_end
			}
		}).sort('datestamp', -1))
	

	@staticmethod
	def to_object(entry: dict):
		return Entry(id=entry["_id"], title=entry["title"], body=entry["body"], tags=entry["tags"], datestamp=entry["datestamp"])
	

	@staticmethod
	def to_presentation_object(entry: dict):
		return Entry(id=entry["_id"], title=entry["title"], body=entry["body"], tags=', '.join(entry["tags"]), datestamp=entry["datestamp"].strftime("%Y-%m-%d %H:%M"))