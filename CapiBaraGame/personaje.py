import pygame
import  constantes
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




    def movimiento(self,delta_x,delta_y):
        posicion_pantalla = [0,0]
        if delta_x < 0:
            self.flip = True
        if delta_x >0:
            self.flip = False

        self.forma.x = self.forma.x + delta_x
        self.forma.y = self.forma.y + delta_y

        #logica solo aplica al jugador y no enemigos
        if self.tipo == 1:
        #Actualizar la pantalla basado la posicion del jugador
        #mover la camara izquierda o derecha
            if self.forma.right > (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA):
                posicion_pantalla[0] = (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA) -self.forma.right
                self.forma.right = constantes.ANCHO_VENTANA -constantes.LIMITE_PANTALLA
            if self.forma.left <  constantes.LIMITE_PANTALLA:
                posicion_pantalla[0] =  constantes.LIMITE_PANTALLA -self.forma.left
                self.forma.left = constantes.LIMITE_PANTALLA
            return  posicion_pantalla


    def update(self):
        #Comprobar si el personaje ha muerto
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False


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
        pygame.draw.rect(interfaz,constantes.COLOR_PERSONAJE,self.forma,1)
