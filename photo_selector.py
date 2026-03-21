from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import shutil 

root = Tk()
root.withdraw()

carpeta_fotos = filedialog.askdirectory(title="Elegí la carpeta de fotos")                   
carpeta_favoritos = filedialog.askdirectory(title="Elegí la carpeta para tus FAVORITAS")
                                        
extensiones = (
    '.jpg', '.jpeg', '.png', '.avif', '.tiff', '.tif', '.webp', '.heic',
    '.cr2', '.cr3', '.nef', '.arw', '.raf', '.dng', '.rw2', '.orf', '.raw'
)
archivos = sorted(
    [a for a in os.listdir(carpeta_fotos) if a.lower().endswith(extensiones)]
)

indice_actual = 0

ventana = root
ventana.deiconify()

label = Label(ventana)
label.pack()

def mostrar_imagen():
    global foto
    global img
    archivo = archivos[indice_actual]
    ruta = os.path.join(carpeta_fotos, archivo) 
    ruta_favoritos = os.path.join(carpeta_favoritos, archivo) 

    img = Image.open(ruta)
    img.thumbnail((800,800))

    foto = ImageTk.PhotoImage(img) 

    label.config(image=foto)
    
    if os.path.exists(ruta_favoritos):
        root.title(f'Foto {indice_actual + 1} de {len(archivos)} - {archivo} - ❤️')
    else:
        root.title(f'Foto {indice_actual + 1} de {len(archivos)} - {archivo}')

def siguiente(event=None): 
    global indice_actual
    if indice_actual < len(archivos) -1:
        indice_actual += 1
        mostrar_imagen()

def anterior(event=None):
    global indice_actual
    if indice_actual > 0:
        indice_actual -= 1
        mostrar_imagen()

def marcar_favorito(event=None):
    global carpeta_fotos
    global carpeta_favoritos
    global indice_actual
    archivo = archivos[indice_actual]
    origen = os.path.join(carpeta_fotos, archivo)
    destino = os.path.join(carpeta_favoritos, archivo)
    
    if os.path.exists(destino):
        try:
            os.remove(destino)
            print('Imagen eliminada de favoritos')
            root.title(f'Foto {indice_actual + 1} de {len(archivos)} - {archivo}')
        except Exception as e:
            print(f'No se pudo borrar de favoritos: {e}')
    else:
        try:
            shutil.copy(origen, destino)
            root.title(f'Foto {indice_actual + 1} de {len(archivos)} - {archivo} - ❤️')
            print(f'Se copio con éxito!')
        except Exception as e:
            root.title(f'Foto {indice_actual + 1} de {len(archivos)} - {archivo} - ERROR AL COPIAR 🤬')
            print(f'Hubo un error: {e}')

def finalizar(event=None):
    fotos_elegidas = os.listdir(carpeta_favoritos)
    total = len(fotos_elegidas)
    
    cartel = Toplevel(ventana)
    cartel.title("Resumen Final")
    cartel.geometry("300x150") # Le damos un tamaño fijo
    
    texto = f'Terminaste de seleccionar las fotos, muy bien!!! \n Cantidad de fotos seleccionadas: {total}. \n Ahora mucha suerte editando!!💖✨'
    Label(cartel, text=texto, pady=20).pack()
    
    Button(cartel, text="Cerrar Programa", command=ventana.destroy).pack()
    
    cartel.grab_set() 

def rotar(event=None):
    global img, foto 
    img = img.rotate(-90, expand=True) 
  
    archivo = archivos[indice_actual]
    ruta = os.path.join(carpeta_fotos, archivo)
    img.save(ruta) 
  
    img.thumbnail((700, 700)) 
    
    foto = ImageTk.PhotoImage(img)
   
    label.config(image=foto)

boton_siguiente = Button(ventana, text="Siguiente", command=siguiente)
boton_siguiente.pack(side=RIGHT)

boton_anterior = Button(ventana, text="Anterior", command=anterior)
boton_anterior.pack(side=LEFT)

boton_favorito = Button(ventana, text='<3', command=marcar_favorito, bg='#f5706e', highlightbackground='#f5706e')
boton_favorito.pack(side=BOTTOM, pady=5) 

boton_fin = Button(ventana, text="Finalizar", command=finalizar, bg="#3498db",  highlightbackground='#3498db')
boton_fin.pack(side=BOTTOM, pady=10)

boton_rotar = Button(ventana, text="⟳ Rotar", command=rotar)
boton_rotar.place(relx=1.0, x=-20, y=20, anchor=NE) 


ventana.bind('<Right>', siguiente)
ventana.bind('<Left>', anterior)
ventana.bind('<space>', marcar_favorito)
ventana.bind('<Return>', finalizar)
ventana.bind('r', rotar)

ventana.focus_set() 
mostrar_imagen()
ventana.mainloop()