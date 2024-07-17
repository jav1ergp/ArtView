import cv2
import face_recognition
import os
from tkinter import simpledialog

def obtener_nombre_usuario():
    username = simpledialog.askstring("Nombre", "Por favor, introduce tu nombre:")
    return username

def obtenerCarasUsuarios():
    carasRegistradas = {}
    for cara in os.listdir('./caras'):
        nombre = os.path.splitext(cara)[0]
        ruta = os.path.join('caras', cara)
        img = face_recognition.load_image_file(ruta)
        encoding = face_recognition.face_encodings(img)
        if len(encoding) > 0: #Si encuentra una cara
            carasRegistradas[nombre] = encoding[0]
    return carasRegistradas

def reconocimientoFacial():
    username = ''
    cam = cv2.VideoCapture(0)
    clasificador = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    caras_registradas = obtenerCarasUsuarios() #obtener las caras registradas
    
    while True:
        ret, frame = cam.read()
        
        if not ret:
            print("No he podido leer el frame")
            break
        
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        caras = clasificador.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in caras:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 255), 3)
            
        cv2.imshow('Detector de caras', frame)
        
        if cv2.waitKey(1) == ord(' '):
            break

        # Convertir la imagen a RGB para la detección de caras
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detectar las ubicaciones de las caras en la imagen y codificarlas
        ubicaciones = face_recognition.face_locations(rgb_frame)
        codificaciones = face_recognition.face_encodings(rgb_frame, ubicaciones)
        
        # Comprobar si alguna de las caras detectadas coincide con las caras registradas
        Coinciden = False
        for codificacion in codificaciones:
            for nombre, encoding in caras_registradas.items():
                coincidencias = face_recognition.compare_faces([encoding], codificacion) 
                
                # Si hay una coincidencia, se ha identificado la cara
                if coincidencias[0]:
                    Coinciden = True
                    username = nombre
                    break
            
            if Coinciden:
                break

        if Coinciden:
            print(f"Bienvenido: {username}")
            break
        
        # Se cea un nuevo usuario cuando no coincide
        if len(caras) > 0:
            username = obtener_nombre_usuario()
            if username is not None and username != "":
                ruta_archivo = os.path.join('caras', f'{username}.jpg')
                cv2.imwrite(ruta_archivo, frame)
                print(f"Nuevo usuario: {ruta_archivo}")
            break
    
    cam.release()
    cv2.destroyAllWindows()
    
    return username

