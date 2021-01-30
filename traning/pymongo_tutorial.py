import pymongo
conn = pymongo.MongoClient()

db = conn.test
print(db.name)
