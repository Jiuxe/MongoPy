import pymongo
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

MONGO_HOST = 'localhost'
MONGO_PORT = "27017"
TIMEOUT = 1000

MONGO_URI = "mongodb://" + MONGO_HOST + ":" + MONGO_PORT + "/"

MONGO_DB = "escuela"
MONGO_DB_COLLECTION = "alumnos"

def getData():
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=TIMEOUT)
        print("Connected to MongoDB")

        bd = client[MONGO_DB]
        collection = bd[MONGO_DB_COLLECTION]

        for doc in collection.find():
            table.insert('',0,text=doc["_id"],values=doc["nombre"])

        client.close()
    except pymongo.errors.ServerSelectionTimeoutErrror as e:
        print("Timeout error: " + str(e))
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: " + e)

window = Tk()


table = ttk.Treeview(window,columns=2)
table.grid(row=1, column=0,columnspan=2)

table.heading("#0", text="ID")
table.heading("#1", text="NOMBRE")
# table.heading("#2", text="SEXO")
# table.heading("#3", text="CALIFICACION")

getData()



window.mainloop()