import speech_recognition as sr
import time

def escuchar():
    texto = ''
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.listen(source, phrase_time_limit=5)

    try:
        texto = r.recognize_google(audio, language="es-ES")
        
    except sr.UnknownValueError:
        texto = None
    except sr.RequestError:
        texto = None
        
    if texto is not None:
        texto = str.lower(texto)
        print("Texto reconocido: ", texto)
        time.sleep(2)
            

    return texto
