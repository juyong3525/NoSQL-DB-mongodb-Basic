import pymongo
conn = pymongo.MongoClient()    # connect local mongodb
knowledge = conn.knowledge    # db
knowledge_it = knowledge.it    # collection


# # update_one
# knowledge_it.update_one(
#     {"author": "Dave"},
#     {"$set":
#         {"age": 40}
#      }
# )


# # update_many
# knowledge_it.update_many(
#     {"author": "Yong"},
#     {"$set": {"age": 25}}
# )
