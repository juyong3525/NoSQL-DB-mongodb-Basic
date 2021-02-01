import pymongo
conn = pymongo.MongoClient()    # connect local mongodb
knowledge = conn.knowledge    # db
knowledge_it = knowledge.it    # collection


# # Collection에 있는 Documents 수
# print(knowledge_it.estimated_document_count())
# print(knowledge_it.count_documents({"author": "Yong"}))


# # find_one
# print(knowledge_it.find_one({"author": "Yong"}))


# # find
# docs = knowledge_it.find()
# for doc in docs:
#     print(doc)


# # sort 함수와 함께 쓰기
# for post in knowledge_it.find().sort("age"):
#     print(post)
