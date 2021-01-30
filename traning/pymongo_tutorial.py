import pymongo
conn = pymongo.MongoClient()

knowledge = conn.knowledge

knowledge_it = knowledge.it

knowledge_it.insert_one(
    {
        "author": "Pong",
        "age": 25
    }
)
