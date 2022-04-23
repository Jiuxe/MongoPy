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

# Definimos las variables de la Base de Datos

client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=TIMEOUT)
bd = client[MONGO_DB]
collection = bd[MONGO_DB_COLLECTION]

def clearData():
    register = table.get_children()
    for reg in register:
        table.delete(reg)

def getData():
    try:
        clearData()
        for doc in collection.find():
            table.insert('',0,text=doc["_id"],values=doc["nombre"])
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: " + e)

def createStudent():
    if len(nombre.get()) != 0 and len(calificacion.get()) != 0 and len(sexo.get()) != 0:
        try:
            doc = {
                "nombre": nombre.get(),
                "sexo": sexo.get(),
                "calificacion": calificacion.get()
            }
            collection.insert_one(doc)
            nombre.delete(0, END)
            sexo.delete(0, END)
            calificacion.delete(0, END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Error", "Debe llenar todos los campos")
    getData()
# Definimos la ventana principal

window = Tk()

table = ttk.Treeview(window,columns=2)
table.grid(row=1, column=0,columnspan=2)

table.heading("#0", text="ID")
table.heading("#1", text="NOMBRE")
# table.heading("#2", text="SEXO")
# table.heading("#3", text="CALIFICACION")

Label(window, text="Nombre").grid(row=2, column=0)
nombre = Entry(window)
nombre.grid(row=2, column=1)

Label(window, text="Sexo").grid(row=3, column=0)
sexo = Entry(window)
sexo.grid(row=3, column=1)

Label(window, text="Calificacion").grid(row=4, column=0)
calificacion = Entry(window)
calificacion.grid(row=4, column=1)

getData()

button_create = Button(window, text="Crear alumno", command=createStudent, bg="green", fg="white")
button_create.grid(row=5, columnspan=2)


window.mainloop()

print("Fin del programa")
client.close()
