from pymongo import MongoClient
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://ihanamo:hanahm22@cluster0.lkhehcb.mongodb.net/?retryWrites=true&w=majority"
# uri = "mongodb+srv://ihanamo:hanahm22@cluster0.lkhehcb.mongodb.net/?retryWrites=true&w=majority"
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






# write_to_mongodb(uri, database, collection, object_to_save)


def read_from_mongodb(uri, database, collection, filter={}):
    # Create a new client and connect to the server
    client = MongoClient(uri)

    try:
        # Connect to the specified database
        db = client[database]

        # Access the specified collection
        coll = db[collection]

        # Find documents based on the filter
        documents = coll.find(filter)

        # Print the found documents
        for document in documents:
            print(document)

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the client connection
        client.close()




# read_from_mongodb(uri, database, collection, filter)
