import math
import random

import pygame

import Constants


class Weapon():

    def __init__(self,image,imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagenOriginal = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagenOriginal,self.angulo)
        self.forma = self.imagen.get_rect()
        self.dispara = False
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self,personaje):
        disparo_cooldown = Constants.COOLDOWN_BALAS
        bala = None
        self.forma.center = personaje.forma.center

        if personaje.flip==False:
            self.forma.x = self.forma.x + personaje.forma.width/4
            self.rotarArma(False)

        if personaje.flip==True:
            self.forma.x = self.forma.x - personaje.forma.width / 4
            self.rotarArma(True)

        #mover la pistola con mouse
        mouse_pos = pygame.mouse.get_pos()
        distancia_x= mouse_pos[0] -self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)

        self.angulo = math.degrees(math.atan2(distancia_y,distancia_x))

        #print(self.angulo)

        #detectar click mouse
        if pygame.mouse.get_pressed()[0] and self.dispara == False and (pygame.time.get_ticks()-self.ultimo_disparo>=disparo_cooldown):
            bala = Bullet(self.imagen_bala,self.forma.centerx,self.forma.centery,self.angulo)
            self.dispara = True
            self.ultimo_disparo = pygame.time.get_ticks()
        #resetear click
        if pygame.mouse.get_pressed()[0] == False:
            self.dispara = False

        return bala

    def rotarArma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.imagenOriginal, True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagenOriginal, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)


    def dibujar(self,interfaz):
        self.imagen = pygame.transform.rotate(self.imagen,self.angulo)
        interfaz.blit(self.imagen,self.forma)
        #pygame.draw.rect(interfaz,Constants.COLOR_ARMA,self.forma,1)


class Bullet (pygame.sprite.Sprite):
    def __init__(self,image,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagenOriginal = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagenOriginal,self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        #calculo de la velocidad bala
        self.delta_x = math.cos(math.radians(self.angulo))*Constants.VELOCIDAD_BALA
        self.delta_y = -math.sin(math.radians(self.angulo)) * Constants.VELOCIDAD_BALA

    def update(self,lista_enemigos):
        daño = 0
        pos_daño = None

        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        if self.rect.right < 0 or self.rect.left > Constants.WINDOW_WIDTH or self.rect.bottom<0 or self.rect.top>Constants.WINDOW_HEIGHT:
            self.kill()

        #verificar colision con enemigos
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                daño = 15 + random.randint(-7,7)
                pos_daño = enemigo.forma
                enemigo.energia -= daño
                self.kill()
                break
        return daño,pos_daño

    def dibujar(self,interfaz):
        interfaz.blit(self.image,(self.rect.centerx,self.rect.centery-int(self.image.get_height())))