import pygame
import constantes
from personaje import Personaje
from textos import DamageText
from weapon import Weapon
from items import Item
from mundo import Mundo
import os
import csv


#funciones:
#escalar imagen

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image,(w*scale,h*scale))
    return nueva_imagen

#funcion para contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))




#funcion listar nombres elementos
def nombres_carpetas(directorio):
    return os.listdir(directorio)


pygame.init()

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA,constantes.ALTO_VENTANA))

pygame.display.set_caption("Nombre del juego")

#variables
posicion_pantalla = [0,0]


#fuentes
font = pygame.font.Font("Assets//fonts//QuinqueFive.ttf",10)
font_game_over = pygame.font.Font("Assets//fonts//QuinqueFive.ttf",24)

game_over_text = font_game_over.render('Juego Terminado', True, constantes.BLANCO)

#Importar imagenes
#Energia
tree_vacio = pygame.image.load("Assets//Images//items//heart_empty.png").convert_alpha()
tree_vacio = escalar_img(tree_vacio,constantes.SCALA_TREE)
tree_mitad = pygame.image.load("Assets//Images//items//heart_half.png").convert_alpha()
tree_mitad = escalar_img(tree_mitad,constantes.SCALA_TREE)
tree_lleno = pygame.image.load("Assets//Images//items//heart_full.png").convert_alpha()
tree_lleno = escalar_img(tree_lleno,constantes.SCALA_TREE)


#Personaje
animaciones = []
for i in range (6):
    img = pygame.image.load(f"Assets//Images//Characters//Player//player-run{i+1}.png")
    img = escalar_img(img,constantes.SCALA_PERSONAJE)
    animaciones.append(img)


#enemigos
directorio_enemigos = "Assets//Images//Characters//enemies"
tipo_enemigos = nombres_carpetas(directorio_enemigos)
animaciones_enemigos = []
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"Assets//Images//Characters//enemies//{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{eni}_{i+1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constantes.SCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    animaciones_enemigos.append(lista_temp)


#Arma
imagen_pistola = pygame.image.load(f"Assets//Images//Weapons//tabanca.png")
imagen_pistola = escalar_img(imagen_pistola,constantes.SCALA_PISTOLA)

#Balas
imagen_balas = pygame.image.load(f"Assets//Images//Weapons//bullet.png")
imagen_balas = escalar_img(imagen_balas,constantes.SCALA_BALA)

#cargar imagenes del mundo
tile_list = []
for x in range(constantes.TILE_TYPES):
    tile_image = pygame.image.load(f"Assets//Images//tiles//tile_{x+1}.png")
    tile_image = pygame.transform.scale(tile_image,(constantes.TILE_SIZE,constantes.TILE_SIZE))
    tile_list.append(tile_image)

#cargar imagenes de los items
potatoe = pygame.image.load("Assets//Images//items//potatoe.png")
potatoe = escalar_img(potatoe,0.05)

coin_images = []
ruta_img = "Assets/Images/items/coin"
num_coin_images = contar_elementos(ruta_img)
print(f"numero de imagenes de monedas: {num_coin_images}")
for i in range(num_coin_images):
    img = pygame.image.load(f"Assets//Images//items//coin//coin_{i}.png")
    img = escalar_img(img,1)
    coin_images.append(img)

def dibujar_texto (texto,fuente,color,x,y):
    img = fuente.render(texto,True,color)
    ventana.blit(img,(x,y))

def vida_jugador():
    c_mitad_dibujado = False
    for i in range(4):
        if jugador.energia >= ((i+1)*25):
            ventana.blit(tree_lleno,(5+i*30,5))
        elif jugador.energia % 25 > 0 and c_mitad_dibujado == False:
            ventana.blit(tree_mitad,(5+i*30,5))
            c_mitad_dibujado = True
        else:
            ventana.blit(tree_vacio,(5+i*30,5))

world_data = []

fila = [51]* constantes.COLUMNAS
for fila in range(constantes.FILAS):
    filas = [51] * constantes.COLUMNAS
    world_data.append(filas)

#cargar el archivo con el nivel
with open("Assets//nivel//mapa_peru.csv",newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x,fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data[x][y] = int(columna)

world = Mundo()
world.process_data(world_data,tile_list)

def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana,constantes.BLANCO,(x*constantes.TILE_SIZE,0),(x*constantes.TILE_SIZE,constantes.ALTO_VENTANA))
        pygame.draw.line(ventana, constantes.BLANCO, (0, x*constantes.TILE_SIZE), (constantes.ANCHO_VENTANA, x*constantes.TILE_SIZE))

#crar un jufador de la clase personaje
jugador = Personaje(100,80,animaciones,70,1)

#crear un enemigo de la clase personaje
cazador = Personaje(400,300,animaciones_enemigos[0],100,2)#si se quieres otro enemigo seria animaciones_enemigos[0]
cazador1 = Personaje(100,200,animaciones_enemigos[0],100,2)

#crear lista de enemigos
lista_enemigos = []
lista_enemigos.append(cazador)
lista_enemigos.append(cazador1)

#crear un arma de la clase weapon
pistola = Weapon(imagen_pistola,imagen_balas)

#crear un grupo de sprites
grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()

moneda = Item(350,25,0,coin_images)
papa = Item(380,55,1,[potatoe])

grupo_items.add(moneda)
grupo_items.add(papa)

#definir las variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False


#controlar el frame rate
reloj = pygame.time.Clock()


run = True

while run == True:

    #QUE VAYA A 60 FPS
    reloj.tick(constantes.FPS)
    ventana.fill(constantes.COLOR_BG)
    #dibujar_grid()

    if jugador.vivo == True:
        #Calcular el movimiento del jugador
        delta_x = 0
        delta_y = 0

        if mover_derecha == True:
            delta_x = constantes.VELOCIDAD
        if mover_izquierda == True:
            delta_x = -constantes.VELOCIDAD
        if mover_arriba == True:
            delta_y = -constantes.VELOCIDAD
        if mover_abajo == True:
            delta_y = constantes.VELOCIDAD

        #mover al jugador
        posicion_pantalla = jugador.movimiento(delta_x,delta_y, world.obstaculos_tiles)

        #Actualizar mapa
        world.update(posicion_pantalla)

        #Actualizar estado del jugador
        jugador.update()
        # Actualizar estado del enemigo
        for ene in lista_enemigos:
            ene.update()

        #Actualiza el estado del arma
        bala = pistola.update(jugador)
        if bala:
            grupo_balas.add(bala)
        for bala in grupo_balas:
            damage,pos_damage = bala.update(lista_enemigos, world.obstaculos_tiles)
            if damage:
                damage_text = DamageText(pos_damage.centerx,pos_damage.centery, str(damage),font,constantes.ROJO)
                grupo_damage_text.add(damage_text)


        #actualizar daño
        grupo_damage_text.update(posicion_pantalla)

        #actualizar item
        grupo_items.update(posicion_pantalla, jugador)

    # dibujar mundo
    world.draw(ventana)

    #dibujar al jugador
    jugador.dibujar(ventana)

    #dibujar al enemigo
    for ene in lista_enemigos:
        if ene.energia == 0:
            lista_enemigos.remove(ene)
        if ene.energia > 0:
            ene.enemigos(jugador, world.obstaculos_tiles, posicion_pantalla)
            ene.dibujar(ventana)

    #dibujar el arma
    pistola.dibujar(ventana)

    #dibujar balas
    for bala in grupo_balas:
        bala.dibujar(ventana)

    #dibujar las vidas
    vida_jugador()

    #dibujar textos
    grupo_damage_text.draw(ventana)
    dibujar_texto(f"Puntuacion: {jugador.score}",font,(255,255,0),500,5)

    #dibujar items
    grupo_items.draw(ventana)

    if jugador.vivo == False:
        ventana.fill(constantes.ROJO_OSCURO)
        text_rect = game_over_text.get_rect(center=(constantes.ANCHO_VENTANA / 2,
                                                    constantes.ALTO_VENTANA / 2))
        ventana.blit(game_over_text, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

        #Para cuando se suelta la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False
    pygame.display.update()

pygame.quit()