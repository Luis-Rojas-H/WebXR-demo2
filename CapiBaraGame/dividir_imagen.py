from PIL import Image
import os

def dividir_guardar_imagen(ruta_imagen, carpeta_destino, divisiones_por_columna):
    # Cargar la imagen
    with Image.open(ruta_imagen) as img:
        ancho, alto = img.size

        # Calcular el tamaño del cuadrado
        tamano_cuadrado = alto // divisiones_por_columna
        divisiones_por_fila = ancho // tamano_cuadrado

        # Crear carpeta de destino si no existe
        os.makedirs(carpeta_destino, exist_ok=True)

        # Dividir y guardar cada tile
        contador = 0
        for i in range(divisiones_por_fila):
            for j in range(divisiones_por_columna):
                # Coordenadas del cuadrado
                izquierda = j * tamano_cuadrado
                superior = i * tamano_cuadrado
                derecha = izquierda + tamano_cuadrado
                inferior = superior + tamano_cuadrado

                # Cortar y guardar el cuadrado
                cuadrado = img.crop((izquierda, superior, derecha, inferior))
                nombre_archivo = f"tile_{contador + 1}.png"
                cuadrado.save(os.path.join(carpeta_destino, nombre_archivo))
                contador += 1

# Llamada a la función
dividir_guardar_imagen("Assets/Images/tiles/map.png", "Assets/Images/tiles/", 8)
