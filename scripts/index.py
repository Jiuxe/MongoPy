import pymongo


MONGO_HOST = 'localhost'
MONGO_PORT = "27017"
TIMEOUT = 1000


MONGO_URI = "mongodb://" + MONGO_HOST + ":" + MONGO_PORT + "/"

MONGO_DB = "escuela"
MONGO_DB_COLLECTION = "alumnos"

try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=TIMEOUT)
    print("Connected to MongoDB")

    bd = client[MONGO_DB]
    collection = bd[MONGO_DB_COLLECTION]

    for doc in collection.find():
        print("Nombre: " + doc['nombre'] + " Sexo: " + doc['sexo'] + " Calificacion: " + str(doc['calificacion']))

    client.close()
except pymongo.errors.ServerSelectionTimeoutErrror as e:
    print("Timeout error: " + str(e))
except pymongo.errors.ConnectionFailure as e:
    print("Could not connect to MongoDB: " + e)