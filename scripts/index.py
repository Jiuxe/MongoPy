import pymongo
from bson.objectid import ObjectId
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

MONGO_HOST = 'localhost'
MONGO_PORT = "27017"
TIMEOUT = 1000

MONGO_URI = "mongodb://" + MONGO_HOST + ":" + MONGO_PORT + "/"

MONGO_DB = "escuela"
MONGO_DB_COLLECTION = "alumnos"
ID_ALUMNO = ""

# Definimos las variables de la Base de Datos
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=TIMEOUT)
bd = client[MONGO_DB]
collection = bd[MONGO_DB_COLLECTION]

def clearData():
    register = table.get_children()
    for reg in register:
        table.delete(reg)

def refreshEntry():
    nombre.delete(0, END)
    sexo.delete(0, END)
    calificacion.delete(0, END)

def getData():
    try:
        clearData()
        for doc in collection.find():
            table.insert('',0,text=doc["_id"],values=doc["nombre"])
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: " + e)


# Funciones CRUD
def createStudent():
    if len(nombre.get()) != 0 and len(calificacion.get()) != 0 and len(sexo.get()) != 0:
        try:
            doc = {
                "nombre": nombre.get(),
                "sexo": sexo.get(),
                "calificacion": calificacion.get()
            }
            collection.insert_one(doc)
            refreshEntry()
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Error", "Debe llenar todos los campos")

    getData()

def updateStudent():
    if len(nombre.get()) != 0 and len(calificacion.get()) != 0 and len(sexo.get()) != 0:
        try:
            button_edit["state"] = "disabled"
            button_delete["state"] = "disabled"
            button_create["state"] = "normal"

            collection.update_one({"_id": ObjectId(ID_ALUMNO)}, {"$set": {"nombre": nombre.get(), "sexo": sexo.get(), "calificacion": calificacion.get()}})

            refreshEntry()

        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Error", "Debe llenar todos los campos")

    getData()

def deleteStudent():
    try:
        collection.delete_one({"_id": ObjectId(ID_ALUMNO)})
        refreshEntry()
        button_delete["state"] = "disabled"
        button_edit["state"] = "disabled"
        button_create["state"] = "normal"

    except pymongo.errors.ConnectionFailure as error:
        print(error)

    getData()

# Buscar registro
def searchStudent():

    search = {}

    if len(buscarNombre.get()) != 0:
        search["nombre"] = buscarNombre.get()
    if len(buscarSexo.get()) != 0:
        search["sexo"] = buscarSexo.get()
    if len(buscarCalificacion.get()) != 0:
        search["calificacion"] = buscarCalificacion.get()

    if len(search) != 0:
        try:
            clearData()
            for doc in collection.find(search):
                table.insert('',0,text=doc["_id"],values=doc["nombre"])
        except pymongo.errors.ConnectionFailure as error:
            print(error)


# Eventos
def doubleClickTable(event):
    global ID_ALUMNO
    ID_ALUMNO = str(table.item(table.selection())["text"])
    doc = collection.find_one({"_id": ObjectId(ID_ALUMNO)})

    refreshEntry()

    nombre.insert(0, doc["nombre"])
    sexo.insert(0, doc["sexo"])
    calificacion.insert(0, doc["calificacion"])

    button_edit["state"] = "normal"
    button_delete["state"] = "normal"
    button_create["state"] = "disabled"


# Definimos la ventana principal
window = Tk()

table = ttk.Treeview(window,columns=2)
table.grid(row=1, column=0,columnspan=2)

table.heading("#0", text="ID")
table.heading("#1", text="NOMBRE")
# table.heading("#2", text="SEXO")
# table.heading("#3", text="CALIFICACION")

table.bind("<Double-Button-1>",doubleClickTable)

Label(window, text="Nombre").grid(row=2, column=0)
nombre = Entry(window)
nombre.grid(row=2, column=1,sticky=W+E)
nombre.focus()

Label(window, text="Sexo").grid(row=3, column=0)
sexo = Entry(window)
sexo.grid(row=3, column=1,sticky=W+E)

Label(window, text="Calificacion").grid(row=4, column=0)
calificacion = Entry(window)
calificacion.grid(row=4, column=1,sticky=W+E)

getData()

button_create = Button(window, text="Crear alumno", command=createStudent, bg="green", fg="white")
button_create.grid(row=5, columnspan=2,sticky=W+E)

button_edit = Button(window, text="Editar alumno", command=updateStudent, bg="yellow", fg="black")
button_edit.grid(row=6, columnspan=2,sticky=W+E)
button_edit["state"] = "disabled"

button_delete = Button(window, text="Eliminar alumno", command=deleteStudent, bg="red", fg="white")
button_delete.grid(row=7, columnspan=2,sticky=W+E)
button_delete["state"] = "disabled"

# Funciones para busqueda de registros

Label(window, text="Buscar Nombre").grid(row=8, column=0)
buscarNombre = Entry(window)
buscarNombre.grid(row=8, column=1,sticky=W+E)
buscarNombre.focus()

Label(window, text="Buscar Sexo").grid(row=9, column=0)
buscarSexo = Entry(window)
buscarSexo.grid(row=9, column=1,sticky=W+E)

Label(window, text="Buscar Calificacion").grid(row=10, column=0)
buscarCalificacion = Entry(window)
buscarCalificacion.grid(row=10, column=1,sticky=W+E)

button_search = Button(window, text="Buscar alumno", command=searchStudent, bg="blue", fg="white")
button_search.grid(row=11, columnspan=2,sticky=W+E)

window.mainloop()

print("Fin del programa")
client.close()
