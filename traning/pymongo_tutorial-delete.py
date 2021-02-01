import pymongo
conn = pymongo.MongoClient()
knowledge = conn.knowledge
knowledge_it = knowledge.it


# # Delete_one
# knowledge_it.delete_one({"author": "Yong"})


# # Delete_many
# knowledge_it.delete_many({"author": "Yong"})
