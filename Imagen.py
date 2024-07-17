from tkinter import filedialog
from PIL import Image

def abrir_imagen(userdir):

    # Abrir cuadro de diálogo para seleccionar una imagen
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.tif")])

    if ruta_imagen:
        # Cargar la imagen seleccionada
        imagen = Image.open(ruta_imagen)
            
            # Abrir cuadro de diálogo para guardar la imagen
        name = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.tif")],
                                            initialdir=userdir,
                                            initialfile="NOMBRE.png")
        if name:
            # Guardar la imagen en el nombre de archivo especificado
            imagen.save(name)
            imagen.close()
            return True
        else:
            imagen.close()
        
    return False

