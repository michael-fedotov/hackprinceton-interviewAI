import datetime

from pymongo import MongoClient

cluster = "mongodb+srv://jacobcardoso2003:1zNz02Yng4ktFoqC@cluster1.xzwx6n8.mongodb.net/test?retryWrites=true&w=majority&appName=Cluster1"
client = MongoClient(cluster)
print(client.list_database_names())

db = client.test

print(db.list_collection_names())

todo1 = {
    "name": "Patrick",
    "text": "my first todo!",
    "status": "open",
    "tags": ["python", "coding"],
    "date": datetime.datetime.utcnow(),
}

todos = db.todos

result = todos.insert_one(todo1)