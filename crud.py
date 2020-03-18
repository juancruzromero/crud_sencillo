from tkinter import *
from tkinter import messagebox
import sqlite3

def conexionBBDD():
    miConexion=sqlite3.connect("Usuarios")
    miCursor=miConexion.cursor()

    try:
        miCursor.execute('''
            CREATE TABLE DATOSUSUARIOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE VARCHAR(50),
            PASSWORD VARCHAR(50),
            COMENTARIOS VARCHAR(100))
            ''')
        messagebox.showinfo("BBDD", "BBDD Creada con éxito")
    except:
        messagebox.showwarning("ERROR FATAL","LA BASE DE DATOS YA EXISTE, FORRE!" )

def salirApp():
    valor = messagebox.askquestion('Salir','Desea salir de la App')
    if valor =="yes":
        root.destroy()

def limpiarCampos():
    
    miID.set("")
    miNombre.set("")
    miPass.set("")
    texto.delete(1.0,END)

def crear(): #Evitar inyección SQL. Pildoras iformaticas (PHP/MySQL del 47 al 53)
    miConexion = sqlite3.connect('Usuarios')
    miCursor = miConexion.cursor()
    
    datos=miNombre.get(), miPass.get(), texto.get("1.0",END)
    #miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES(NULL,'" + miNombre.get() +
    #"','" + miPass.get() +
    #"','" + texto.get("1.0", END) + "')")
    miCursor.execute("INSERT INTO DATOSUSUARIOS VALUES (NULL,?,?,?)",(datos))
    miConexion.commit()
    messagebox.showinfo("BBDD","Registro Insertado")

def leer():
    miConexion = sqlite3.connect('Usuarios')
    miCursor = miConexion.cursor()
    miCursor.execute("SELECT * FROM DATOSUSUARIOS WHERE ID =" + miID.get())
    elUsuario = miCursor.fetchall()#Lista lo que está en la BBDD

    for usuario in elUsuario:
        miID.set(usuario[0])
        miNombre.set(usuario[1])
        miPass.set(usuario[2])
        texto.insert(1.0,usuario[3])
    miConexion.commit()

def actualizar():
        miConexion = sqlite3.connect('Usuarios')
        miCursor = miConexion.cursor()
        miCursor.execute("UPDATE DATOSUSUARIOS SET NOMBRE='" + miNombre.get() +
        "', PASSWORD = '" + miPass.get() +
        "', COMENTARIOS = '" + texto.get("1.0",END) +
        "' WHERE ID=" + miID.get())
        miConexion.commit()
        messagebox.showinfo("BBDD","Registro Actualizado")

def borrar():
        miConexion = sqlite3.connect('Usuarios')
        miCursor = miConexion.cursor()
        miCursor.execute("DELETE FROM DATOSUSUARIOS WHERE ID =" + miID.get())
        miConexion.commit()
        messagebox.showinfo("BBDD","Registro Borrado")

root = Tk()
#------------------------------BARRA MENÚ------------------------------
barraMenu = Menu(root)
root.config(menu=barraMenu, width = 300, height = 300)

bbddMenu = Menu(barraMenu, tearoff=0)
bbddMenu.add_command(label="Conectar", command=conexionBBDD)
bbddMenu.add_command(label="Salir", command=salirApp)

borrarMenu = Menu(barraMenu, tearoff=0)
borrarMenu.add_command(label="Borrar campos", command=limpiarCampos)

crudMenu = Menu(barraMenu, tearoff=0)
crudMenu.add_command(label="Crear", command = crear)
crudMenu.add_command(label="Actualizar",command=actualizar)
crudMenu.add_command(label="Borrar", command=borrar)

ayudaMenu = Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Licencia")
ayudaMenu.add_command(label="Acerca de...")

barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
barraMenu.add_cascade(label="Borrar", menu=borrarMenu)
barraMenu.add_cascade(label="Crud", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

#------------------------------CAMPOS------------------------------
miFrame = Frame(root)
miFrame.pack()

miID= StringVar()
miNombre = StringVar()
miPass = StringVar()

cuadroID = Entry(miFrame, textvariable = miID)
cuadroID.grid(row=0, column=1, padx=10,pady=10)

cuadroNombre = Entry(miFrame, textvariable = miNombre)
cuadroNombre.grid(row=1, column=1, padx=10,pady=10)
cuadroNombre.config(justify="right")

cuadroPass = Entry(miFrame, textvariable = miPass)
cuadroPass.grid(row=2, column=1, padx=10,pady=10)
cuadroPass.config(show="*")

texto=Text(miFrame, height=5, width=16)
texto.grid(row=3, column=1, padx=10,pady=10)
scroll =Scrollbar(miFrame, command=texto.yview)
scroll.grid(row=3, column=2, sticky="nsew")

texto.config(yscrollcommand=scroll.set)

#------------------------------LABELS(Texto)------------------------------

idLabel = Label(miFrame,text='ID:')
idLabel.grid(row=0,column=0,sticky="e", padx=10,pady=10)

nombreLabel = Label(miFrame,text='Nombre:')
nombreLabel.grid(row=1,column=0,sticky="e", padx=10,pady=10)

passLabel = Label(miFrame,text='Contraseña:')
passLabel.grid(row=2,column=0,sticky="e", padx=10,pady=10)

textLabel = Label(miFrame,text='Texto:')
textLabel.grid(row=3,column=0,sticky="e", padx=10,pady=10)

#------------------------------BOTONES------------------------------

miFrame2= Frame(root)
miFrame2.pack()

botonCrear=Button(miFrame2, text='Create', command = crear)
botonCrear.grid(row=1,column=0,sticky="e", padx=10, pady=10)

botonLeer=Button(miFrame2, text='Read', command=leer)
botonLeer.grid(row=1,column=1,sticky="e", padx=10, pady=10)

botonActualizar=Button(miFrame2, text='Update', command=actualizar)
botonActualizar.grid(row=1,column=2,sticky="e", padx=10, pady=10)

botonBorrar=Button(miFrame2, text='Delete', command=borrar)
botonBorrar.grid(row=1,column=3,sticky="e", padx=10, pady=10)

#Siempre al final
root.mainloop()