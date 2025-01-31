import math

import pygame

import Constants



class Personaje:
    def __init__(self,x,y,animaciones,energia):
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        #imagen de la animacion que s emuestra actualmente
        self.frame_index = 0
        #horaactual en milisegundos desde el inicio de pygame
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center =(x,y)
        self.golpe = False
        self.ultimo_gole = pygame.time.get_ticks()


    #actualizar las imagenes para hacer la animacion
    def update(self):
        #comprobar si el personajemurio
        if self.energia<=0:
            self.energia=0
            self.vivo=False

        #timer para recibir daño again
        golpe_cooldown = 1000
        if self.golpe == True:
            if pygame.time.get_ticks() -self.ultimo_gole>golpe_cooldown:
                self.golpe = False

        cooldownAnimacion = 100
        self.image = self.animaciones[self.frame_index]

        if pygame.time.get_ticks() - self.update_time >= cooldownAnimacion:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0


    def dibujar(self,interfaz):
        imagen_flip = pygame.transform.flip(self.image,self.flip,False)
        #dibujar imagen
        interfaz.blit(imagen_flip,self.forma)
        pygame.draw.rect(interfaz,Constants.COLOR_PERSONAJE,self.forma,1)

    def moverEnemigos(self,jugador):
        ene_dx = 0
        ene_dy = 0

        #distancia con el jugador
        distancia = math.sqrt(((self.forma.centerx - jugador.forma.centerx)**2)+(self.forma.centery - jugador.forma.centery)**2)

        if self.forma.centerx > jugador.forma.centerx:
            ene_dx = -Constants.VELOCIDAD_ENEMIGO
        if self.forma.centerx < jugador.forma.centerx:
            ene_dx = Constants.VELOCIDAD_ENEMIGO
        if self.forma.centery > jugador.forma.centery:
            ene_dy = -Constants.VELOCIDAD_ENEMIGO
        if self.forma.centery < jugador.forma.centery:
            ene_dy = Constants.VELOCIDAD_ENEMIGO

        self.movimiento(ene_dx,ene_dy)

        if distancia < Constants.RANGO_ATAQUE and jugador.golpe == False:
            jugador.energia -=5
            jugador.golpe = True
            jugador.ultimo_golpe = pygame.time.get_ticks()



    def movimiento(self,deltaX,deltaY):

        if deltaX<0:
            self.flip = True
        if deltaX>0:
            self.flip = False

        if self.forma.left < 0:
            self.forma.left = 0
        if self.forma.right > Constants.WINDOW_WIDTH:
            self.forma.right = Constants.WINDOW_WIDTH
        if self.forma.top < 0:
            self.forma.top = 0
        if self.forma.bottom > Constants.WINDOW_HEIGHT:
            self.forma.bottom = Constants.WINDOW_HEIGHT

        self.forma.x= self.forma.x + deltaX
        self.forma.y = self.forma.y + deltaY