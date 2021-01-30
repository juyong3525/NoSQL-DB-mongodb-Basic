import pymongo
conn = pymongo.MongoClient()

knowledge = conn.knowledge

knowledge_it = knowledge.it

post = {"author": "Mike", "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"]}
knowledge_it.insert_one(post)
