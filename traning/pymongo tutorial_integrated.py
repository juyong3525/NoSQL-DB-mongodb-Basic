import pymongo
conn = pymongo.MongoClient()
books = conn.books
it_book = books.it_book

# # CRUD - Insert
# data = list()
# for index in range(100):
#     data.append({"author": "yong", "publisher": "yong.org", "number": index})
# it_book.insert_many(data)


# CRUD - Read
docs = it_book.find()
for doc in docs:
    print(doc)


# # CRUD - Update
# it_book.update_many({}, {"$set": {"publisher": "www.yong.org"}})


# # CRUD - Delete
# it_book.delete_many({"number": {"$gte": 6}})
