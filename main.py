import os
import pygame
import Constants
from Personaje import Personaje
from textos import DamageText
from weapon import Weapon

#funciones
#funcion escalar
def escalarImagen(imagen,escala):
    w = imagen.get_width()
    h = imagen.get_height()

    nuevaImagen = pygame.transform.scale(imagen,(w*escala,h*escala))
    return nuevaImagen

#funcioon contar elementos
def contarElementos(directorio):
    return len(os.listdir(directorio))

#funcion listar nombres elementos
def nombresCarpetas(directorio):
    return os.listdir(directorio)

#iniciar juego
pygame.init()
window = pygame.display.set_mode((Constants.WINDOW_WIDTH,Constants.WINDOW_HEIGHT))
pygame.display.set_caption("KodlandTest")

#fuentes
font = pygame.font.Font("assets/fonts/Kubasta.ttf",25)
font_game_over = pygame.font.Font("assets/fonts/Kubasta.ttf",100)
font_reinicio = pygame.font.Font("assets/fonts/Kubasta.ttf",30)
font_inicio = pygame.font.Font("assets/fonts/Kubasta.ttf",30)
font_titulo = pygame.font.Font("assets/fonts/Kubasta.ttf",75)

game_over_text = font_game_over.render("GAME OVER!",True,Constants.BLANCO)
text_reinicio = font_reinicio.render("Reiniciar",True,Constants.NEGRO)

#botones de inicio
boton_jugar = pygame.Rect(Constants.WINDOW_WIDTH/2 -100,Constants.WINDOW_HEIGHT/2-50,200,50)
boton_salir = pygame.Rect(Constants.WINDOW_WIDTH/2 -100,Constants.WINDOW_HEIGHT/2+50,200,50)

texto_boton_jugar = font_inicio.render("Jugar",True,Constants.NEGRO)
texto_boton_salir = font_inicio.render("Salir",True,Constants.BLANCO)

#pantalla de inicio
def pantalla_inicio():
    window.fill(Constants.COLOR_BG)
    dibujarTexto("KODLAND-GAME",font_titulo,Constants.BLANCO,Constants.WINDOW_WIDTH/2-200, Constants.WINDOW_HEIGHT/2-200)
    pygame.draw.rect(window,Constants.AMARILLO,boton_jugar)
    pygame.draw.rect(window,Constants.AMARILLO,boton_salir)
    window.blit(texto_boton_jugar,(boton_jugar.x+50,boton_jugar.y ))
    window.blit(texto_boton_salir,(boton_salir.x+50,boton_salir.y ))
    pygame.display.update()




#importar imagenes
#ENERGIA
corazon_vacio = pygame.image.load("assets/images/items/heart_3.png").convert_alpha()
corazon_vacio =escalarImagen(corazon_vacio,Constants.ESCALA_CORAZON)
corazon_mitad = pygame.image.load("assets/images/items/heart_2.png").convert_alpha()
corazon_mitad =escalarImagen(corazon_mitad,Constants.ESCALA_CORAZON)
corazon_lleno = pygame.image.load("assets/images/items/heart_1.png").convert_alpha()
corazon_lleno = escalarImagen(corazon_lleno,Constants.ESCALA_CORAZON)
#animaciones personaje
animaciones=[]
for i in range (7):
    img = pygame.image.load(f"assets//images//character//frame_{i+1}.png")
    img = escalarImagen(img,Constants.ESCALA_PERSONAJE)
    animaciones.append(img)

#enemigos
directorio_enemigos = "assets//images//character//enemies"
tipo_enemigos = nombresCarpetas(directorio_enemigos)
#animaciones enemigos
animaciones_enemigos =[]
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets//images//character//enemies//{eni}"
    num_animaciones = contarElementos(ruta_temp)
    for i in range (num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//frame_{i+1}.png").convert_alpha()
        img_enemigo=escalarImagen(img_enemigo,Constants.ESCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)

    animaciones_enemigos.append(lista_temp)


#armas
imagen_pistola = pygame.image.load("assets//images//armas//gun.png")
imagen_pistola = escalarImagen(imagen_pistola,Constants.ESCALA_ARMA)

#Balas
imagen_balas = pygame.image.load("assets//images//armas//bullet.png")
imagen_balas = escalarImagen(imagen_balas,Constants.ESCALA_BALA)
#finanimaciones

def dibujarTexto(texto,fuente,color,x,y):
    img = fuente.render(texto,True,color)
    window.blit(img,(x,y))

def vidaJugador():
    c_mitad_dibujado = False
    for i in range(4):
        if jugador.energia >= ((i+1)*25):
            window.blit(corazon_lleno,(5+i*50,5))
        elif jugador.energia % 25 > 0 and c_mitad_dibujado == False:
            window.blit(corazon_mitad,(5+i*50,5))
            c_mitad_dibujado = True
        else:
            window.blit(corazon_vacio, (5 + i * 50, 5))

def dibujarGrid():
    for x in range(30):
        pygame.draw.line(window,Constants.BLANCO,(x*40,0),(x*40,Constants.WINDOW_HEIGHT))
        pygame.draw.line(window,Constants.BLANCO,(0,x*40),(Constants.WINDOW_WIDTH,x*40))



#instancia de personaje
#jugador
jugador = Personaje(Constants.PERSONAJE_WIDTH,Constants.PERSONAJE_HEIGHT,animaciones,100)
#enemigo phantom
phantom = Personaje(400,300,animaciones_enemigos[0],100)
phantom2 = Personaje(400,100,animaciones_enemigos[0],100)

#lista de enemigos
lista_enemigos = []
lista_enemigos.append(phantom)
lista_enemigos.append(phantom2)



#instancia de weapon
pistola = Weapon(imagen_pistola,imagen_balas)

#crear un grupo de sprites
grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()


#movimiento variables
moverArriba = False
moverAbajo = False
moverIzquierda = False
moverDerecha = False

#controlar el frame rate
reloj = pygame.time.Clock()
boton_reinicio = pygame.Rect(Constants.WINDOW_WIDTH/2-100, Constants.WINDOW_HEIGHT/2+100,200,50)

mostrar_inicio = True
run = True
while run:

    if mostrar_inicio:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                if boton_salir.collidepoint(event.pos):
                    run = False
    else:

        #velocidad a 60FPS
        reloj.tick(Constants.FPS)

        window.fill(Constants.COLOR_BG)

        # dibujarGrid
        dibujarGrid()

        if jugador.vivo:


            #calcular movimiento jugador
            deltaX = 0
            deltaY = 0

            if moverDerecha == True:
                deltaX=Constants.VELOCIDAD
            if moverIzquierda == True:
                deltaX = -Constants.VELOCIDAD
            if moverArriba == True:
                deltaY = -Constants.VELOCIDAD
            if moverAbajo == True:
                deltaY = Constants.VELOCIDAD

            #mover jugador
            jugador.movimiento(deltaX, deltaY)



            #actualiza estado jugador
            jugador.update()
            #actualizar estado enemigo
            for ene in lista_enemigos:
                ene.update()
                print(ene.energia)


            #actualiza estado arma
            bala = pistola.update(jugador)
            if bala:
                grupo_balas.add(bala)

            for bala in grupo_balas:
                damage,pos_damage = bala.update(lista_enemigos)
                if damage:
                    damage_text = DamageText(pos_damage.centerx,pos_damage.centery,str(damage),font,Constants.ROJO)
                    grupo_damage_text.add(damage_text)
            #actualizar daño
            grupo_damage_text.update()


        #dibujar jugador
        jugador.dibujar(window)
        #dibujar enemigos
        for ene in lista_enemigos:
            if ene.energia <= 0:
                lista_enemigos.remove(ene)
            if ene.energia > 0:
                ene.moverEnemigos(jugador)
                ene.dibujar(window)

        #dibujar arma
        pistola.dibujar(window)
        #dibujarBala
        for bala in grupo_balas:
            bala.dibujar(window)

        #dibujar corazones
        vidaJugador()



        #dibujarTexto


        #dibujar texto
        grupo_damage_text.draw(window)

        if jugador.vivo == False:
            window.fill(Constants.ROJO_OSCURO)
            text_rect = game_over_text.get_rect(center=(Constants.WINDOW_WIDTH/2,Constants.WINDOW_HEIGHT/2))

            window.blit(game_over_text,text_rect)


            pygame.draw.rect(window,Constants.AMARILLO,boton_reinicio)
            window.blit(text_reinicio,(boton_reinicio.x + 30,boton_reinicio.y ))

        for event in pygame.event.get():
            #cierra el juego
            if event.type == pygame.QUIT:
                run = False

            #controlar cuando el jugador se mueve
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moverIzquierda = True
                if event.key == pygame.K_d:
                    moverDerecha = True
                if event.key == pygame.K_w:
                    moverArriba = True
                if event.key == pygame.K_s:
                    moverAbajo = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moverIzquierda = False
                if event.key == pygame.K_d:
                    moverDerecha = False
                if event.key == pygame.K_w:
                    moverArriba = False
                if event.key == pygame.K_s:
                    moverAbajo = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio.collidepoint(event.pos) and not jugador.vivo:
                    jugador.vivo = True
                    jugador.energia = 100


                    for ene in lista_enemigos:
                        if ene.energia <= 0:
                            lista_enemigos.remove(ene)
                        if ene.energia > 0:
                            ene.moverEnemigos(jugador)
                            ene.dibujar(window)

        pygame.display.update()

pygame.quit()