from pymongo import MongoClient
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://ihanamo:hanahm22@cluster0.lkhehcb.mongodb.net/?retryWrites=true&w=majority"
database = "test"
collection = "user"
# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def write_to_mongodb(object_to_save):
    print(object_to_save)
    client = MongoClient(uri)

    try:
        db = client[database]

        coll = db[collection]

        result = coll.insert_one(object_to_save)

        print("Document inserted with ID:", result.inserted_id)

    except Exception as e:
        print("Error:", e)

    finally:
        client.close()


def read_from_mongodb(filter={}):
    client = MongoClient(uri)

    try:
        db = client[database]

        coll = db[collection]

        documents = coll.find(filter)

        for document in documents:
            print(document)

    except Exception as e:
        print("Error:", e)

    finally:
        client.close()

