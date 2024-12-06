import pygame
from pygame.draw_py import clip_line

import  constantes
import math
#from main import posicion_pantalla


class Personaje():
    def __init__(self,x,y,animaciones,energia,tipo):
        self.score = 0
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        #Imagen de la animacion que se esta mostrando actualmente
        self.frame_index = 0
        #Aqui se almacena la hora actual (en milisegundos desde que se inició `pygame`)
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x,y)
        self.tipo = tipo
        self.golpe = False
        self.ultimo_golpe = pygame.time.get_ticks()

    def movimiento(self, delta_x, delta_y, obstaculos_tiles):
        posicion_pantalla = [0, 0]
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        # Movimiento horizontal
        self.forma.x += delta_x
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = obstacle[1].left
                if delta_x < 0:
                    self.forma.left = obstacle[1].right

        # Movimiento vertical
        self.forma.y += delta_y
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = obstacle[1].top
                if delta_y < 0:
                    self.forma.top = obstacle[1].bottom

        # Lógica de cámara (solo para el jugador)
        if self.tipo == 1:
            # Movimiento horizontal de la cámara
            if self.forma.right > (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA):
                desplazamiento = (self.forma.right - (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA)) * 0.5
                posicion_pantalla[0] -= desplazamiento
                self.forma.right = constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA
            elif self.forma.left < constantes.LIMITE_PANTALLA:
                desplazamiento = (constantes.LIMITE_PANTALLA - self.forma.left) * 0.5
                posicion_pantalla[0] += desplazamiento
                self.forma.left = constantes.LIMITE_PANTALLA

            # Movimiento vertical de la cámara
            if self.forma.bottom > (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA):
                desplazamiento = (self.forma.bottom - (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA)) * 0.5
                posicion_pantalla[1] -= desplazamiento
                self.forma.bottom = constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA
            elif self.forma.top < constantes.LIMITE_PANTALLA:
                desplazamiento = (constantes.LIMITE_PANTALLA - self.forma.top) * 0.5
                posicion_pantalla[1] += desplazamiento
                self.forma.top = constantes.LIMITE_PANTALLA

            return posicion_pantalla

    def enemigos(self, jugador, obstaculos_title, posicion_pantalla):
        clipped_line = ()
        ene_dx = 0
        ene_dy = 0
        self.forma.x += posicion_pantalla[0]
        self.forma.y += posicion_pantalla[1]

        linea_de_vision = ((self.forma.centerx, self.forma.centery),
                           (jugador.forma.centerx, jugador.forma.centery))

        for obs in obstaculos_title:
            if obs[1].clipline(linea_de_vision):
                clipped_line = obs[1].clipline(linea_de_vision)


        distancia = math.sqrt((self.forma.centerx - jugador.forma.centerx)**2 +
                              (self.forma.centery - jugador.forma.centery)**2)

        if not clipped_line and distancia < constantes.RANGO:
            if self.forma.centerx > jugador.forma.centerx:
                ene_dx = -constantes.VELOCIDAD_ENEMIGO
            if self.forma.centerx < jugador.forma.centerx:
                ene_dx = constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery > jugador.forma.centery:
                ene_dy = -constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery < jugador.forma.centery:
                ene_dy = constantes.VELOCIDAD_ENEMIGO

        self.movimiento(ene_dx, ene_dy, obstaculos_title)

        #atacar al jugador
        if distancia < constantes.RANGO_ATAQUE and jugador.golpe == False:
            jugador.energia -= 25
            jugador.golpe = True
            jugador.ultimo_golpe = pygame.time.get_ticks()

    def update(self):
        #Comprobar si el personaje ha muerto
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False

        #time para poder volver a recibir daño
        golpe_cooldown = 1000
        if self.tipo == 1:
            if self.golpe == True:
                if pygame.time.get_ticks() - self.ultimo_golpe > golpe_cooldown:
                    self.golpe = False


        cooldown_animacion = 120
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def dibujar(self,interfaz):
        imagen_flip = pygame.transform.flip(self.image,self.flip,False)
        interfaz.blit(imagen_flip,self.forma)
        #pygame.draw.rect(interfaz,constantes.COLOR_PERSONAJE,self.forma,1)
