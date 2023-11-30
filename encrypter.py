from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os, shutil, threading

#Ventana
ventana = tk.Tk()
ventana.resizable(False, False)
ventana.title("File Encrypter")

#Checks
contenedor_nombre = str()
passw = None
checkbuttons, checkstates = [], []
y_coor = 12

#Funciones
#Encriptacion
def cargar_clave(archivo_clave):
    with open(archivo_clave, 'rb') as archivo:
        return archivo.read()

def guardar_clave(clave, archivo_clave):
	try:
		with open(archivo_clave, 'wb') as archivo:
			archivo.write(clave)
	except:
		os.makedirs(".passwords")
		with open(archivo_clave, 'wb') as archivo:
			archivo.write(clave)

def encriptar_archivo(path, name):
	with open(path, "rb") as archivo_original:
		contenido = archivo_original.read()
	
	contenido_encriptado = passw.encrypt(contenido)
	
	with open(".files/" + contenedor_nombre + "/" + name, "wb") as archivo_encriptado:
		archivo_encriptado.write(contenido_encriptado)
	borrar_checkbutton(0)

def desencriptar_archivo(archivos):
	global contenedor_nombre
	while True:
		password = simpledialog.askstring("Confirm password", "Password of " + contenedor_nombre + ": ", show = "*")
		if password is not None:
			if verif_password_correct(contenedor_nombre, password):
				path = filedialog.askdirectory()
				if path is not None:
					global passw
					for archivo in archivos:
						with open(".files/" + contenedor_nombre + "/" + archivo, 'rb') as archivo_encriptado:
							contenido_encriptado = archivo_encriptado.read()
			
						contenido_desencriptado = passw.decrypt(contenido_encriptado)
			
						with open(path + "/" + archivo, 'wb') as archivo_desencriptado:
							archivo_desencriptado.write(contenido_desencriptado)
					messagebox.showinfo("Success", "Files deencrypted succesfully.")
					break
				else:
					break
			else:
				messagebox.showinfo("Error", "Incorrect password.")
		else:
			break

#Archivos
def agregar_archivos():
	archivos = filedialog.askopenfilenames()
	for archivo in archivos:
		encriptar_archivo(archivo, os.path.basename(archivo))
		give_index()

def borrar_archivos(archivos):
	for archivo in archivos:
		os.remove(".files/" + contenedor_nombre + "/" + archivo)

#Contenedores
def abrir_contenedor(name):
	while True:
		password = simpledialog.askstring("Confirm password", "Password of " + name + ": ", show = "*")
		if password is not None:
			if verif_password_correct(name, password):
				global contenedor_nombre, checkbuttons, checkstates, y_coor
				y_coor = 12
				
				if name == contenedor_nombre:
					messagebox.showinfo("Container", "The container was already open.")
					break
				messagebox.showinfo("Success.", "Container opened succesfully.")
				ventana.title("Container: " + name)
				path = ".files/" + name + "/"
				
				for checkbutton in checkbuttons:
					checkbutton.destroy()
				checkbuttons, checkstates = [], []
				
				index = 0
				for archivo in os.listdir(path):
					if os.path.isfile(os.path.join(path, archivo)) and archivo[0] != '.':
						update_check(archivo, index)
						index += 1
				contenedor_nombre = name
				canvas.config(scrollregion=(0, 0, 346, y_coor - 11))
				archivo_menu.entryconfigure("Add files", state = "normal")
				archivo_menu.entryconfigure("Deencrypt files", state = "normal")
				archivo_menu.entryconfigure("Delete files", state = "normal")
				break
			else:
				messagebox.showinfo("Error", "Incorrect password.")
		else:
			break

#Interfaz
#Contraseña
def verif_name():
	while True:
		name = simpledialog.askstring("Create container", "Name of the container: ")
		if name is not None:
			if name in carpetas:
				messagebox.showinfo("Error", "Container already exists.")
			else:
				return name
		else:
			break
			
def verif_password_equal():
	while True:
		password1 = simpledialog.askstring("Create container", "Password: ", show = "*")
		if password1 is not None:
			password2 = simpledialog.askstring("Create container", "Confirm password: ", show = "*")
			if password2 is not None:
				if password1 == password2:
					return password1
				else:
					messagebox.showinfo("Error", "The passwords don't match.")
			else:
				break
		else:
			break

def verif_password_correct(name, password):
	clave = cargar_clave(".passwords/" + name + ".key")
	f = Fernet(clave)
	
	try:
		with open(".files/" + name + "/." + name + ".verif", "rb") as file:
			contenido_encriptado = file.read()
	except:
		messagebox.showinfo("Error", "Key file not found.")
		return 
		
	contenido_desencriptado = f.decrypt(contenido_encriptado)
	if contenido_desencriptado.decode() == password:
		global passw
		passw = f
		return True
	else:
		return False

#Contenedor
def create_contenedor():
	name = verif_name()
	if name is not None:
		password = verif_password_equal()
		if password is not None:
			os.mkdir(".files/" + name)
			clave = Fernet.generate_key()
			f = Fernet(clave)
			contenido_encriptado = f.encrypt(password.encode())
			with open(".files/" + name + "/." + name + ".verif", 'wb') as archivo_encriptado:
				archivo_encriptado.write(contenido_encriptado)
			archivo_clave = ".passwords/" + name + ".key"
			guardar_clave(clave, archivo_clave)
			messagebox.showinfo("Success", "Container created succesfully.")
			lista_contenedores.add_command(label = name, command = lambda: abrir_contenedor(name))
			lista_borrar.add_command(label = name, command = lambda: verif_delete_contenedor(name))
			carpetas.append(name)

def verif_delete_contenedor(name):
	while True:
		password = simpledialog.askstring("Confirm deletion.", "Password of the container:", show = '*')
		if password is not None:
			if verif_password_correct(name, password):
				messagebox.showinfo("Success", "Container deleted succesfully.")
				shutil.rmtree(".files/" + name)
				os.remove(".passwords/" + name + ".key")
				
				#Eliminar opcion
				index = None
				for i, label in enumerate(carpetas):
					if label == name:
						index = i
						break
				if index is not None:
					lista_contenedores.delete(index)
					lista_borrar.delete(index)
					carpetas.pop(index)
				global contenedor_nombre
				contenedor_nombre = str()
				break
			elif False:
				messagebox.showinfo("Error", "Incorrect password.")
		else:
			break

#Checks
def on_configure(event):
    canvas.configure(scrollregion = canvas.bbox("all"))

def give_index():
	global y_coor, checkbuttons, checkstates
	for checkbutton in checkbuttons:
		checkbutton.destroy()
	checkbuttons, checkstates = [], []
	y_coor, index = 12, 0
	path = ".files/" + contenedor_nombre + "/"
	for archivo in os.listdir(path):
		if os.path.isfile(os.path.join(path, archivo)) and archivo[0] != '.':
			update_check(archivo, index)
			index += 1
	canvas.config(scrollregion=(0, 0, 346, y_coor - 11))

def update_check(elemento, index):
	borrar_checkbutton(index)
	create_check(elemento)

def check_states(option):
	global checkstates, checkbuttons
	clickeados = []
	for i, estado in enumerate(checkstates):
		if estado.get() == 1:
			clickeados.append(checkbuttons[i]["text"])
	if not clickeados:
		messagebox.showinfo("Error", "You must select at least one file from the container.")
		return
	else:
		if option == "delete":
			borrar_archivos(clickeados)
		else:
			desencriptar_archivo(clickeados)
			messagebox.showinfo("Success", "Files deencrypted succesfully.")
		give_index()

def create_check(elemento):
	global checkbuttons, y_coor
	var = tk.IntVar()
	checkbutton = tk.Checkbutton(canvas, text = elemento, bg = "#999999", width = 40, anchor = "w", variable = var)
	canvas.create_window((0, y_coor), window = checkbutton, anchor = "w")
	y_coor += 23
	checkbuttons.append(checkbutton)
	checkstates.append(var)

def borrar_checkbutton(indice):
    global checkbuttons
    if 0 <= indice < len(checkbuttons):
        checkbutton = checkbuttons.pop(indice)
        checkbutton.destroy()

def salir():
	ventana.destroy()

#Interfaz
#Menu
barra_menu = tk.Menu(ventana, bg = "#333333", fg = "white")
ventana.config(menu = barra_menu)

#Frame
frame = tk.Frame(ventana)
frame.pack(fill = "both", expand = True)

#Canvas
canvas = tk.Canvas(frame, width = 346, height = 400, bg = "#000011")
canvas.pack(side = "left", fill = "both", expand = True)

#Scrollbar
scrollbar = tk.Scrollbar(frame, command = canvas.yview)
scrollbar.pack(side = "right", fill = "y")
canvas.configure(yscrollcommand = scrollbar.set)

#Items menú
#Archivo
archivo_menu = tk.Menu(barra_menu, bg = "#333333", fg = "white", tearoff = 0)
archivo_menu.add_command(label = "Add files", state = "disabled", command = agregar_archivos)
archivo_menu.add_command(label = "Deencrypt files", state = "disabled", command = lambda: check_states("decrypt"))
archivo_menu.add_command(label = "Delete files", state = "disabled", command = lambda: check_states("delete"))
barra_menu.add_cascade(label = "File", menu = archivo_menu)

#Carpetas
try:
	carpetas = os.listdir(".files")
	carpetas = [elemento for elemento in carpetas if os.path.isdir(os.path.join(".files/", elemento))]
except:
	os.makedirs(".files")
	carpetas = os.listdir(".files")
	carpetas = [elemento for elemento in carpetas if os.path.isdir(os.path.join(".files/", elemento))]

#Contenedor
menu_contenedor = tk.Menu(barra_menu, bg = "#333333", fg = "white", tearoff = 0)
barra_menu.add_cascade(label = "Containers", menu = menu_contenedor)

#Contenedores
lista_contenedores = tk.Menu(menu_contenedor, bg = "#333333", fg = "white", tearoff = 0)
lista_borrar = tk.Menu(menu_contenedor, bg = "#333333", fg = "white", tearoff = 0)
menu_contenedor.add_cascade(label = "Open container", menu = lista_contenedores)
menu_contenedor.add_command(label = "Create container", command = create_contenedor)
menu_contenedor.add_cascade(label = "Delete container", menu = lista_borrar)

for carpeta in carpetas:
	lista_contenedores.add_command(label = carpeta, command = lambda carpeta = carpeta: abrir_contenedor(carpeta))
	lista_borrar.add_command(label = carpeta, command = lambda carpeta = carpeta: verif_delete_contenedor(carpeta))

#Salir
barra_menu.add_command(label = "Exit", command = salir)

canvas.bind("<Configure>", on_configure)

ventana.mainloop()
