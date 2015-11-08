from pymongo import MongoClient
import time

conn = MongoClient('localhost',27017)
db = conn.get_database("mytest")
collection = db.get_collection("books")
i = 0;

while True:
    if i>1000:
        break
    i += 1
    collection.insert({"name":'nn'+str(i)})
    time.sleep(0.01)