import pymongo
conn = pymongo.MongoClient()

knowledge = conn.knowledge

knowledge_it = knowledge.it

# Collection에 있는 Documents 수
print(knowledge_it.estimated_document_count())
