from PIL import Image
import os

def dividir_guardar_imagen(ruta_imagen, carpeta_destino, tamano_cuadrado, filas, columnas):
    # Cargar la imagen
    with Image.open(ruta_imagen) as img:
        ancho, alto = img.size

        # Validar si las dimensiones de la imagen son correctas
        if ancho != columnas * tamano_cuadrado or alto != filas * tamano_cuadrado:
            raise ValueError("Las dimensiones de la imagen no coinciden con el tamaño de los cuadros y el número de filas/columnas.")

        # Crear carpeta de destino si no existe
        os.makedirs(carpeta_destino, exist_ok=True)

        # Dividir y guardar cada tile
        contador = 0
        for i in range(filas):
            for j in range(columnas):
                # Coordenadas del cuadro
                izquierda = j * tamano_cuadrado
                superior = i * tamano_cuadrado
                derecha = izquierda + tamano_cuadrado
                inferior = superior + tamano_cuadrado

                # Cortar y guardar el cuadro
                cuadro = img.crop((izquierda, superior, derecha, inferior))
                nombre_archivo = f"tile_{contador + 1}.png"
                cuadro.save(os.path.join(carpeta_destino, nombre_archivo))
                contador += 1

        print(f"Se han guardado {contador} tiles en la carpeta '{carpeta_destino}'.")

# Parámetros de la imagen
ruta_imagen = "Assets/Images/tiles/mapa_peru.png"
carpeta_destino = "Assets/Images/tiles/"
tamano_cuadrado = 32
filas = 16
columnas = 10

# Llamada a la función
dividir_guardar_imagen(ruta_imagen, carpeta_destino, tamano_cuadrado, filas, columnas)