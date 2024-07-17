import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import shutil
import Camara as webcam
import Imagen as images
import reconocimientoVoz as speech 
import reconocimientoCaras as faces 
import os
import cv2
import numpy as np

texto = ''  # Variable que guarda el texto del reconocedor de voz
frame = None 
username = '' # Variable que guarda el username del reconocedor de caras
userdir = '' # Variable que guarda el directorio del usuario
    
def comandos_voz():
    instrucc.pack(pady=10)
    texto = ''
    
    while texto == '':
        texto = speech.escuchar()
        
        if texto == "subir imagen":
            subir_imagen(True)
        elif texto == "abrir cámara":
            abrir_camara(True)
        elif texto == "abrir galería":
            abrir_galeria("eliminar", True)
        elif texto == "cerrar sesión":
            cerrar_sesion()
        elif texto == "cerrar aplicación":
            cerrar_ventana()
        elif texto == "eliminar usuario":
            eliminacion_user("personal")
        else:
            print("Orden no disponible")
            texto = ''

# Distinción del modo con audio y sin audio
def abrir_camara(audio):
    if audio == True:
        abrir_galeria("seleccionar", True)
    else:
        abrir_galeria("seleccionar", False)
    
    
# Ejecuta la camara para detectar el marcador
def ejecucionCamara(ruta_img, audio):
    global frame
    imagen = cv2.imread(ruta_img, cv2.IMREAD_UNCHANGED)

    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Camara')

    if not cap.isOpened():
        print("No se puede abrir la cámara")
        exit()
        
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("No he podido leer el frame")
            break

        resultado = webcam.detectar_aruco(frame, imagen)
        cv2.imshow('Camara', resultado)
            
        if cv2.waitKey(1) == ord(' '):
            break

    cap.release()
    cv2.destroyWindow('Camara')
    
    if audio == True:
        print("¿Nueva orden?")
        comandos_voz()


# Abre la galeria cuando se ha subido una imagen
def subir_imagen(audio):
    if images.abrir_imagen(userdir):
        if audio == True:
            abrir_galeria("eliminar", True)
        else:
            abrir_galeria("eliminar", False)
     
# Abre la camara con la imagen pasada en la ruta
def seleccionar_imagen(ruta, audio):
    ruta = "./galerias/" + username + "/" + ruta
    ejecucionCamara(ruta, audio)
            
            
def abrir_galeria(opcion, audio):    
    ventana = tk.Toplevel(root)
    vt = "Galería de " + username
    ventana.title(vt)
    ventana.geometry("850x700")
    
    # instrucciones
    if opcion == "eliminar" and audio == True:
        txt = "Para eliminar una imagen, diga el nombre del fichero (sin extensión)\n en voz alta una vez se haya cerrado esta ventana (7s).\nSi desea ejecutar otra orden, diga 'nueva orden' \ny después, el comando a realizar."
        instrucc = ttk.Label(ventana, text=txt, style='TLabel')
        instrucc.pack(pady=10)
    elif opcion == "seleccionar" and audio == True:
        txt = "Para seleccionar una imagen, diga el nombre del fichero (sin extensión)\n en voz alta una vez se haya cerrado esta ventana (7s).\nSi desea ejecutar otra orden, diga 'nueva orden' \ny después, el comando a realizar."
        instrucc = ttk.Label(ventana, text=txt, style='TLabel')
        instrucc.pack(pady=10)

    frame_interno = tk.Frame(ventana)
    frame_interno.pack(fill=tk.BOTH, expand=True)

    imagenes = []
    n = 0
    # Guardar imagenes de la galeria
    for archivo in os.listdir(userdir):
        n += 1
        ruta_archivo = os.path.join(userdir, archivo)
        if os.path.isfile(ruta_archivo):
            try:
                imagen = Image.open(ruta_archivo)
                imagen = imagen.resize((125, 125))  #Redimensionar la imagen
                img_tk = ImageTk.PhotoImage(imagen) #La portada
                imagenes.append((img_tk, n, archivo, ruta_archivo))  #Almacenar la imagen y el nombre del archivo
            except Exception as e:
                print(f"No se pudo subir la imagen {ruta_archivo}: {str(e)}")

    num_columnas = 4

    for i, (img_tk, n, fname, ruta) in enumerate(imagenes):
        # Calcular las coordenadas de la celda actual en la cuadrícula
        fila = i // num_columnas
        columna = i % num_columnas

        # Crear un marco para contener la imagen y el texto
        frame = tk.Frame(frame_interno)
        frame.grid(row=fila, column=columna, padx=10, pady=10)

        # Crear imagen
        label_imagen = tk.Label(frame, image=img_tk)
        label_imagen.image = img_tk  
        label_imagen.pack()

        if opcion == "eliminar" and audio == False:
            boton_eliminar = tk.Button(frame, text="Eliminar", command=lambda ruta=ruta: [eliminar_imagen(ruta, False, "galeria", fname), ventana.destroy()])
            boton_eliminar.pack()
        elif opcion == "seleccionar" and audio == False:
            boton_selecc = tk.Button(frame, text="Seleccionar", command=lambda ruta=fname: [seleccionar_imagen(ruta, False), ventana.destroy()])
            boton_selecc.pack()
        # Crear texto
        titulo = str(n) + ") " + fname
        label_nombre = tk.Label(frame, text=titulo)
        label_nombre.pack()
        
    if audio == True:
        ventana.after(7000, lambda: ventana.destroy())
        
    # Espera a que se cierre la ventana antes de ejecutar el código siguiente
    ventana.wait_window()
    
    if audio == True:
        nombre_arch = ''
        print("¿Nombre del archivo?")
        nombre_arch = speech.escuchar()
            
        ruta_arch = ''
        encontrado = False
        nueva_orden = False
        
        while encontrado == False and nueva_orden == False:
            if nombre_arch == "nueva orden":
                nueva_orden = True
                break
            else:
                for img_tk, n, fname, ruta in imagenes:
                    nombre, ext = os.path.splitext(fname) # Para quitar extensión img.jpg
                    if nombre == nombre_arch:
                        ruta_arch = ruta
                        print("Archivo encontrado en " + ruta_arch)
                        encontrado = True
                        break
                else:
                    print("No se encontró ningún archivo con dicho nombre. Pruebe con otro.")
                    nombre_arch = ''
                    print("¿Nombre del archivo?")
                    nombre_arch = speech.escuchar()
                    
        if nueva_orden == True:
            print("¿Nueva orden?")
            comandos_voz()
            
        if encontrado == True and ruta_arch != '':
            if opcion == "eliminar":
                eliminar_imagen(ruta_arch, True, "galeria", nombre_arch)
            elif opcion == "seleccionar": 
               seleccionar_imagen(fname, True)
                

def eliminar_imagen(ruta, audio, opc, nom_galeria):
    try:
        os.remove(ruta)
        
        if opc == "galeria": # Eliminar imagen de la Galeria
            if audio == True:
                abrir_galeria("eliminar", True)
            else:
                abrir_galeria("eliminar", False)
        else: # Eliminar el usuario completo, se elimina tambien su carpeta galeria
            nom_gal, ext = os.path.splitext(nom_galeria) 
            ruta_galeria = os.path.join("galerias", nom_gal)
            try:
                shutil.rmtree(ruta_galeria)
                print("Galería de " + nom_gal + " eliminada exitosamente")
            except OSError as e:
                print("No se pudo eliminar la galería correctamente")
            
            eliminacion_user("admin")
    except Exception as e:
        print(f"No se pudo eliminar la imagen {ruta}: {str(e)}")
        
        
# Ocultar/Mostrar botones segun su estado
def cambiar_estado():
    if boton_estado.get(): # Botón activado
        print("Interfaz sin audio activada")
        for boton in botones_ocultos:
            boton.pack(pady=10)
            
        boton_audio.pack_forget()
    else: # Botón desactivado
        print("Interfaz sin audio desactivada")
        for boton in botones_ocultos:
            boton.pack_forget()
        
        boton_audio.pack(pady=10) 


def identificacion_user():
    global username, userdir
    username = faces.reconocimientoFacial()
    ruta_directorio = os.path.join("galerias", username)
    if username is None:
        print("No se ha creado un nuevo usuario.")
        return
    # Verificar si la galería no existe
    if not os.path.exists(ruta_directorio):
        os.mkdir(ruta_directorio)
        print("Galería creada exitosamente.")
    else:
        print("La galería ya existe.")
        
    userdir = ruta_directorio
    print(userdir)
    
    boton_ventana0.pack_forget()
    boton_ventana00.pack_forget()
    bienv1.pack_forget()
    boton_cerrar_ventana.pack_forget()

    #Cuando termina la identificación muestra el resto de funciones
    bienvenida2 = "¡Bienvenido a la aplicación, " + username + "!"
    bienv2.configure(text=bienvenida2)
    bienv2.pack(pady=20)
    boton_not_audio.pack(pady=20)
    boton_audio.pack(pady=20)
    boton_logout.pack(pady=10)
    boton_elim_user.pack(pady=3)
    boton_cerrar_ventana.pack(pady=3)
    
def cerrar_sesion():
    global username, userdir
    username = ''
    userdir = ''
    bienv1.pack(pady=20)
    boton_ventana0.pack(pady=10)
    boton_ventana00.pack(pady=10)
    boton_cerrar_ventana.pack(pady=10)
    
    instrucc.pack_forget()
    bienv2.pack_forget()
    boton_not_audio.pack_forget()
    boton_audio.pack_forget()
    if boton_estado.get(): # Botón audio activado
        for boton in botones_ocultos:
            boton.pack_forget()
        
    boton_logout.pack_forget()
    boton_elim_user.pack_forget()
    
    
def eliminacion_user(opc):
    if opc == "admin": # Elegir Usuario y eliminarlo
        ventana = tk.Toplevel()
        vt = "Lista de usuarios registrados"
        ventana.title(vt)
        ventana.geometry("850x700")

        frame_interno = tk.Frame(ventana)
        frame_interno.pack(fill=tk.BOTH, expand=True)

        usuarios = []
        n = 0
        #Guardar usuarios
        for archivo in os.listdir("./caras"):
            n += 1
            ruta_archivo = "./caras/" + archivo
            if os.path.isfile(ruta_archivo):
                try:
                    imagen = Image.open(ruta_archivo)
                    imagen = imagen.resize((125, 125))  #Redimensionar la imagen
                    img_tk = ImageTk.PhotoImage(imagen) #La portada
                    usuarios.append((img_tk, n, archivo, ruta_archivo))  #Almacenar la imagen y el nombre del archivo
                except Exception as e:
                    print(f"No se pudo subir la imagen {ruta_archivo}: {str(e)}")

        num_columnas = 4

        for i, (img_tk, n, fname, ruta) in enumerate(usuarios):
            fila = i // num_columnas
            columna = i % num_columnas

            
            frame = tk.Frame(frame_interno)
            frame.grid(row=fila, column=columna, padx=10, pady=10)

            label_imagen = tk.Label(frame, image=img_tk)
            label_imagen.image = img_tk
            label_imagen.pack()

            boton_eliminar = tk.Button(frame, text="Eliminar", command=lambda ruta=ruta: [eliminar_imagen(ruta, False, "usuarios", fname), ventana.destroy()])
            boton_eliminar.pack()

            titulo = str(n) + ") " + fname
            label_nombre = tk.Label(frame, text=titulo)
            label_nombre.pack()
        
        ventana.mainloop()
    else: # Eliminar Usuario Logeado
        img = username + ".jpg"
        ruta_img = os.path.join("caras", img)
        os.remove(ruta_img)  # Eliminar la imagen del usuario
        ruta_galeria = os.path.join("galerias", username)
        try:
            shutil.rmtree(ruta_galeria) # Eliminar la galería también
            print("Galería de " + username + " eliminada exitosamente")
        except OSError as e:
            print("No se pudo eliminar la galería correctamente")
            
        cerrar_sesion()
           
def cerrar_ventana():
    root.destroy() 

# Creación de la ventana principal
root = tk.Tk()
root.title("Aplicación CUIA")

foto_app = Image.open("./iconos/logo_cuia.jpg")
foto_app = foto_app.resize((870, 150))
foto = ImageTk.PhotoImage(foto_app)
label_foto = tk.Label(root, image=foto)
label_foto.pack()

# Estilo
style = ttk.Style()
style.configure('TButton', font=('Trebuchet MS', 12))
style.configure('TLabel', font=('Trebuchet MS', 15))
style.configure('TFrame', background="white")

# Contenedor principal
main_frame = ttk.Frame(root)
main_frame.pack()
main_frame.configure(style="TFrame")

bienvenida1 = "¡Bienvenido/a a la aplicación! ¿Procedemos con la identificación de usuario?"
bienv1 = ttk.Label(main_frame, text=bienvenida1, style='TLabel')
bienv1.pack(pady=20)
bienvenida2 = "¡Bienvenido/a a la aplicación, " + username + "!"
bienv2 = ttk.Label(main_frame, text=bienvenida2, style='TLabel')

boton_ventana0 = ttk.Button(main_frame, text="Adelante", command=identificacion_user)
boton_ventana0.pack(pady=10)
boton_ventana00 = ttk.Button(main_frame, text="Eliminar usuarios", command=lambda: eliminacion_user("admin"))
boton_ventana00.pack(pady=10)
boton_cerrar_ventana = ttk.Button(root, text="Cerrar App", command=cerrar_ventana)
boton_cerrar_ventana.pack(pady=10)

boton_estado = tk.BooleanVar()
not_audio_icono = Image.open("./iconos/not_audio.jpg")
not_audio_icono = not_audio_icono.resize((50, 50))
icono1 = ImageTk.PhotoImage(not_audio_icono)
boton_not_audio = tk.Checkbutton(main_frame, image=icono1, variable=boton_estado, command=cambiar_estado)
audio_icono = Image.open("./iconos/audio.jpg")
audio_icono = audio_icono.resize((50, 50))
icono2 = ImageTk.PhotoImage(audio_icono)

boton_audio = ttk.Button(main_frame, image=icono2, command=comandos_voz)
boton_ventana1 = ttk.Button(main_frame, text="subir imagen", command=lambda: subir_imagen(False))
boton_ventana2 = ttk.Button(main_frame, text="Abrir cámara", command=lambda: abrir_camara(False))
boton_ventana3 = ttk.Button(main_frame, text="Abrir galería", command=lambda: abrir_galeria("eliminar", False))
botones_ocultos = [boton_ventana1, boton_ventana2, boton_ventana3]
boton_logout = ttk.Button(root, text="Cerrar sesión", command=cerrar_sesion)
boton_elim_user = ttk.Button(root, text="Eliminar usuario", command=lambda: eliminacion_user("personal"))

txt = "Lista de órdenes posibles: subir imagen, abrir cámara,abrir galería, cerrar sesión y cerrar aplicacion."
instrucc = ttk.Label(main_frame, text=txt, style='TLabel')

etiqueta_imagen = tk.Label(root)
etiqueta_imagen.pack()
etiqueta_texto = tk.Label(root)
etiqueta_texto.pack()

# Ejecución del bucle principal de la app
root.mainloop()