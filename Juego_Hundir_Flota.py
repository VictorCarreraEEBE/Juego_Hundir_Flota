
import pygame
from pygame.locals import *
import sys
import math
import random
import time


class JuegoHundirFlota:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)

        global ANCHO_VENTANA, ALTO_VENTANA, ventana
        global BLANCO, ROJO, AZUL

        ANCHO_VENTANA, ALTO_VENTANA = 920, 650
        ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

        BLANCO = (240, 240, 250)
        ROJO = (255, 0, 0)
        AZUL = (50, 150, 200)

        self.menu_inicio = MenuInicio(self)
        # self.menu_instrucciones = MenuInstrucciones(self)
        self.juego_principal = JuegoPrincipal(self)
        self.menu_fin_juego = MenuFinJuego(self)

        self.estado_actual = self.menu_inicio
        # self.estado_actual = self.menu_fin_juego

    def ejecutar(self):
        while True:
            self.estado_actual.visualizar_estado()


class Menu:
    def __init__(self, juego):
        self.juego = juego
        self.fuente_texto_botones = pygame.font.Font('Fuentes/Roboto-Black.ttf', 30)
        self.visualizar = False

    def mostrar_botones_principales(self, lista_botones, posicion_raton):
        for boton in lista_botones:
            boton.cambiar_color(posicion_raton)
            boton.mostrar(ventana)


class MenuInicio(Menu):
    def __init__(self, juego):
        Menu.__init__(self, juego)

        self.imagen_fondo = pygame.image.load('Imagenes/Hundir_Flota_principal.jpg').convert()
        self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA-200))
        self.imagen_fondo_rect = self.imagen_fondo.get_rect(midbottom=(ANCHO_VENTANA/2, ALTO_VENTANA))

        self.imagen_remaches = pygame.image.load('Imagenes/remaches.jpg').convert()
        self.imagen_remaches = pygame.transform.scale(self.imagen_remaches, (ANCHO_VENTANA, 200))
        self.imagen_remaches_rect = self.imagen_remaches.get_rect(midtop=(ANCHO_VENTANA/2, 0))

        self.imagen_titulo = pygame.image.load('Imagenes/Imagen_titulo.png').convert_alpha()
        self.imagen_titulo = pygame.transform.scale(self.imagen_titulo, (1212*0.6, 174*0.6))
        self.imagen_titulo_rect = self.imagen_titulo.get_rect(center=(ANCHO_VENTANA / 2, 100))

        self.boton_JUGAR = BotonPrincipal(imagen=None, posicion=(ANCHO_VENTANA/2, 480), entrada_texto="JUGAR",
                                          fuente=self.fuente_texto_botones, color_texto=(0, 0, 0),
                                          color_flotante_texto=ROJO, ancho=500, alto=50, ancho_borde=5, radio_borde=25)
        self.boton_INSTRUCCIONES = BotonPrincipal(imagen=None, posicion=(ANCHO_VENTANA/2, 540),
                                                  entrada_texto="INSTRUCCIONES", fuente=self.fuente_texto_botones,
                                                  color_texto=(0, 0, 0), color_flotante_texto=ROJO, ancho=500, alto=50,
                                                  ancho_borde=5, radio_borde=25)
        self.boton_SALIR = BotonPrincipal(imagen=None, posicion=(ANCHO_VENTANA/2, 600), entrada_texto="SALIR",
                                          fuente=self.fuente_texto_botones, color_texto=(0, 0, 0),
                                          color_flotante_texto=ROJO, ancho=500, alto=50, ancho_borde=5, radio_borde=25)

    def mostrar_elementos(self):
        ventana.blit(self.imagen_fondo, self.imagen_fondo_rect)
        ventana.blit(self.imagen_remaches, self.imagen_remaches_rect)
        ventana.blit(self.imagen_titulo, self.imagen_titulo_rect)

        self.mostrar_botones_principales([self.boton_JUGAR, self.boton_INSTRUCCIONES, self.boton_SALIR],
                                         self.posicion_raton)

    def visualizar_estado(self):
        self.visualizar = True
        clock = pygame.time.Clock()
        while self.visualizar:

            self.posicion_raton = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_JUGAR.raton_encima(self.posicion_raton):
                        self.juego.juego_principal = JuegoPrincipal(self.juego)  # Creamos partida nueva
                        self.juego.estado_actual = self.juego.juego_principal
                        self.visualizar = False
                    # if self.boton_INSTRUCCIONES.raton_encima(self.posicion_raton):
                    #     self.juego.estado_actual = self.juego.menu_instrucciones
                    #     self.visualizar = False
                    if self.boton_SALIR.raton_encima(self.posicion_raton):
                        pygame.quit()
                        sys.exit()

            self.mostrar_elementos()

            pygame.display.update()
            clock.tick(60)


class MenuFinJuego(Menu):
    def __init__(self, juego):
        Menu.__init__(self, juego)

        self.fuente_texto_fin_juego = pygame.font.Font('Fuentes/Anton-Regular.ttf', 50)
        self.fuente_texto_ganador = pygame.font.Font('Fuentes/Roboto-Black.ttf', 50)

        self.imagen_fondo = pygame.image.load('Imagenes/captura_fin_juego.jpg').convert()

        self.capa_transparente = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        self.capa_transparente.fill((0, 0, 0, 230))

        self.superficie_blanca = pygame.Surface((ANCHO_VENTANA, 100))
        self.superficie_blanca.fill(BLANCO)
        self.superficie_blanca_rect = self.superficie_blanca.get_rect(center=(ANCHO_VENTANA/2, ALTO_VENTANA/3))

        self.texto = self.fuente_texto_fin_juego.render("FIN DEL JUEGO", True, (0, 0, 0))
        self.texto_rect = self.texto.get_rect(center=(ANCHO_VENTANA/2, ALTO_VENTANA/3))

        self.texto_ganador = self.fuente_texto_ganador.render('Indeterminado', True, BLANCO)
        self.texto_ganador_rect = self.texto_ganador.get_rect(center=(ANCHO_VENTANA/2, 390))

        self.boton_JUGAR_DE_NUEVO = BotonPrincipal(imagen=None, posicion=(ANCHO_VENTANA/2, 540),
                                                   entrada_texto="JUGAR DE NUEVO", fuente=self.fuente_texto_botones,
                                                   color_texto=(0, 0, 0), color_flotante_texto=ROJO, ancho=500, alto=50,
                                                   ancho_borde=5, radio_borde=25)

        self.boton_VOLVER_MENU_INICIO = BotonPrincipal(imagen=None, posicion=(ANCHO_VENTANA/2, 600),
                                                       entrada_texto="VOLVER AL INICIO",
                                                       fuente=self.fuente_texto_botones,
                                                       color_texto=(0, 0, 0), color_flotante_texto=ROJO, ancho=500,
                                                       alto=50, ancho_borde=5, radio_borde=25)

    def mostrar_elementos(self):
        ventana.blit(self.imagen_fondo, (0, 0))
        ventana.blit(self.capa_transparente, (0, 0))
        ventana.blit(self.superficie_blanca, self.superficie_blanca_rect)
        ventana.blit(self.texto, self.texto_rect)

        if self.juego.juego_principal.ganador_jugador_humano:
            self.texto_ganador = self.fuente_texto_ganador.render('Has ganado!', True, BLANCO)
            self.texto_ganador_rect = self.texto_ganador.get_rect(center=(ANCHO_VENTANA/2, 390))
        else:
            self.texto_ganador = self.fuente_texto_ganador.render('Has perdido :(', True, BLANCO)
            self.texto_ganador_rect = self.texto_ganador.get_rect(center=(ANCHO_VENTANA/2, 390))

        ventana.blit(self.texto_ganador, self.texto_ganador_rect)

        self.mostrar_botones_principales([self.boton_JUGAR_DE_NUEVO, self.boton_VOLVER_MENU_INICIO],
                                         self.posicion_raton)

    def visualizar_estado(self):
        self.visualizar = True
        clock = pygame.time.Clock()
        while self.visualizar:

            self.posicion_raton = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_JUGAR_DE_NUEVO.raton_encima(self.posicion_raton):
                        self.juego.juego_principal = JuegoPrincipal(self.juego)  # Creamos partida nueva
                        self.juego.estado_actual = self.juego.juego_principal
                        self.visualizar = False

                    if self.boton_VOLVER_MENU_INICIO.raton_encima(self.posicion_raton):
                        self.juego.estado_actual = self.juego.menu_inicio
                        self.visualizar = False

            self.mostrar_elementos()

            pygame.display.update()
            clock.tick(60)


class JuegoPrincipal:
    def __init__(self, juego):
        self.juego = juego
        self.jugador_humano = JugadorHumano(self, (110, 210))
        self.jugador_virtual = JugadorVirtual(self, (520, 210))
        self.turno_jugador_humano = True
        self.ganador_jugador_humano = True
        self.game_over = False
        self.visualizar = False

        self.imagen_fondo = pygame.image.load('Imagenes/imagen_fondo.jpg').convert()
        self.imagen_fondo = pygame.transform.scale(self.imagen_fondo, (920, 650))
        self.imagen_fondo_rect = self.imagen_fondo.get_rect(topleft=(0, 0))

    def actualizar_jugada(self, i):
        if self.turno_jugador_humano:
            jugador = self.jugador_humano
            oponente = self.jugador_virtual
        else:
            jugador = self.jugador_virtual
            oponente = self.jugador_humano

        # set miss "M or hit "Tocado"
        if i in oponente.indices_flota:
            jugador.mapa_enemigo[i] = "Tocado"

            # check if ship is sunk("Hundido")
            for ship in oponente.flota:
                sunk = True
                for i in ship.indices:
                    if jugador.mapa_enemigo[i] == "Desconocido":
                        sunk = False
                        break
                if sunk:
                    for i in ship.indices:
                        jugador.mapa_enemigo[i] = "Hundido"
                        ship.ocultado = False

        else:
            jugador.mapa_enemigo[i] = "Agua"
            self.cambiar_turnos()

        # Comprobar game over
        game_over = True
        for i in oponente.indices_flota:
            if jugador.mapa_enemigo[i] == "Desconocido":
                game_over = False
        self.game_over = game_over
        if self.game_over:
            if jugador == self.jugador_virtual:
                self.ganador_jugador_humano = False

    def cambiar_turnos(self):
        if self.turno_jugador_humano:
            self.turno_jugador_humano = False
        else:
            self.turno_jugador_humano = True

    def mostrar_elementos(self, barco_que_movemos=None):
        ventana.blit(self.imagen_fondo, self.imagen_fondo_rect)
        self.jugador_humano.cuadricula.mostrar_cuadricula()
        self.jugador_virtual.cuadricula.mostrar_cuadricula()
        for barco in self.jugador_virtual.flota:
            barco.mostrar_barco()
        for barco in self.jugador_humano.flota:
            barco.mostrar_barco()
        if barco_que_movemos is not None:
            barco_que_movemos.mostrar_barco()

    def visualizar_estado(self):
        self.visualizar = True
        clock = pygame.time.Clock()

        self.jugador_virtual.colocar_barcos()
        self.jugador_virtual.computar_indices_flota()

        self.jugador_humano.colocar_barcos()
        self.jugador_humano.computar_indices_flota()

        current_time = 0
        jugada_time = 0
        while self.visualizar:

            self.posicion_raton = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.turno_jugador_humano \
                            and self.jugador_virtual.cuadricula.raton_en_cuadricula(self.posicion_raton):
                        col, row = self.jugador_virtual.cuadricula.obtener_pos_cuadricula(self.posicion_raton)
                        index = row*10 + col
                        if self.jugador_humano.mapa_enemigo[index] == "Desconocido":
                            self.actualizar_jugada(index)
                            jugada_time = pygame.time.get_ticks()

            if not self.turno_jugador_humano and current_time - jugada_time > self.jugador_virtual.tiempo_disparo:
                self.jugador_virtual.disparar()
                jugada_time = pygame.time.get_ticks()
                pygame.event.clear()

            self.mostrar_elementos()

            self.jugador_humano.dibujar_disparos(self.jugador_virtual)
            self.jugador_virtual.dibujar_disparos(self.jugador_humano)

            if self.game_over:
                time.sleep(1)

                pygame.image.save(ventana, "Imagenes/captura_fin_juego.jpg")

                self.juego.menu_fin_juego = MenuFinJuego(self.juego)
                self.juego.estado_actual = self.juego.menu_fin_juego
                self.visualizar = False

            pygame.display.update()
            current_time = pygame.time.get_ticks()
            clock.tick(60)


class Cuadricula:
    def __init__(self, juego_principal, jugador, start_grid, medida_celda):
        self.juego_principal = juego_principal
        self.jugador = jugador

        self.fuente_texto_coordenadas = pygame.font.Font('Fuentes/PoetsenOne-Regular.ttf', 20)
        self.fuente_texto_titulo = pygame.font.Font('Fuentes/Anton-Regular.ttf', 30)

        self.start_grid = start_grid
        self.MEDIDA_CELDA = medida_celda

        self.IZQUIERDA_CUADRICULA = start_grid[0]
        self.DERECHA_CUADRICULA = start_grid[0] + medida_celda[0] * 10
        self.ARRIBA_CUADRICULA = start_grid[1]
        self.ABAJO_CUADRICULA = start_grid[1] + medida_celda[1] * 10

        self.superficie_rect = pygame.Rect(self.IZQUIERDA_CUADRICULA, self.ARRIBA_CUADRICULA,
                                           self.MEDIDA_CELDA[0]*10, self.MEDIDA_CELDA[1]*10)

        self.capa_transparente = pygame.Surface((self.MEDIDA_CELDA[0]*10, self.MEDIDA_CELDA[1]*10), pygame.SRCALPHA)
        self.capa_transparente.fill((255, 255, 255, 150))

    def mostrar_cuadricula(self):

        ventana.blit(self.capa_transparente, (self.IZQUIERDA_CUADRICULA, self.ARRIBA_CUADRICULA))

        x = self.IZQUIERDA_CUADRICULA
        y = self.ARRIBA_CUADRICULA
        numero_fila = 1
        letra_columna = 'A'
        for n in range(11):
            if n < 10:
                texto_numero_fila = self.fuente_texto_coordenadas.render(str(numero_fila), True, (0, 0, 0))
                texto_numero_fila_rect = texto_numero_fila.get_rect(topright=(self.IZQUIERDA_CUADRICULA - 5, y + 4))
                ventana.blit(texto_numero_fila, texto_numero_fila_rect)

                texto_letra_columna = self.fuente_texto_coordenadas.render(letra_columna, True, (0, 0, 0))
                texto_letra_columna_rect = texto_letra_columna.get_rect(bottomleft=(x + 9, self.ARRIBA_CUADRICULA - 2))
                ventana.blit(texto_letra_columna, texto_letra_columna_rect)

            pygame.draw.line(ventana, (0, 0, 0), (x, self.ARRIBA_CUADRICULA), (x, self.ABAJO_CUADRICULA), 3)
            pygame.draw.line(ventana, (0, 0, 0), (self.IZQUIERDA_CUADRICULA, y), (self.DERECHA_CUADRICULA, y), 3)
            x += self.MEDIDA_CELDA[0]
            y += self.MEDIDA_CELDA[1]
            numero_fila += 1
            letra_columna = chr(ord(letra_columna) + 1)

        if self.jugador == self.juego_principal.jugador_humano:
            texto_titulo_cuadricula = self.fuente_texto_titulo.render('MI FLOTA', True, (150, 0, 0))
            texto_titulo_cuadricula_rect = texto_titulo_cuadricula.get_rect(
                midbottom=(self.IZQUIERDA_CUADRICULA + self.MEDIDA_CELDA[0]*5, self.ARRIBA_CUADRICULA - 50))
            ventana.blit(texto_titulo_cuadricula, texto_titulo_cuadricula_rect)
        else:
            texto_titulo_cuadricula = self.fuente_texto_titulo.render('FLOTA ENEMIGA', True, (150, 0, 0))
            texto_titulo_cuadricula_rect = texto_titulo_cuadricula.get_rect(
                midbottom=(self.IZQUIERDA_CUADRICULA + self.MEDIDA_CELDA[0] * 5, self.ARRIBA_CUADRICULA - 50))
            ventana.blit(texto_titulo_cuadricula, texto_titulo_cuadricula_rect)

    def raton_en_cuadricula(self, posicion_raton):
        if (posicion_raton[0] < self.IZQUIERDA_CUADRICULA or
            posicion_raton[1] < self.ARRIBA_CUADRICULA or
            posicion_raton[0] > self.DERECHA_CUADRICULA or
                posicion_raton[1] > self.ABAJO_CUADRICULA):
            return False
        else:
            return True

    def obtener_pos_cuadricula(self, posicion):
        x = math.floor((posicion[0]-self.IZQUIERDA_CUADRICULA)/self.MEDIDA_CELDA[0])
        y = math.floor((posicion[1]-self.ARRIBA_CUADRICULA)/self.MEDIDA_CELDA[1])
        if x < 0 or y < 0 or x > 9 or y > 9:
            return None
        return x, y

    def pos_cuadricula_a_pos_pantalla(self, posicion_cuadricula):
        x = self.IZQUIERDA_CUADRICULA + (posicion_cuadricula[0] * self.MEDIDA_CELDA[0])
        y = self.ARRIBA_CUADRICULA + (posicion_cuadricula[1] * self.MEDIDA_CELDA[1])
        return x, y


class Jugador:
    def __init__(self, juego_principal, origen_cuadricula):
        self.juego_principal = juego_principal
        self.cuadricula = Cuadricula(self.juego_principal, self, origen_cuadricula, (30, 30))
        self.barco_destructor = Barco('destructor', (110, 550), self.cuadricula)
        self.barco_crucero = Barco('crucero', (200, 550), self.cuadricula)
        self.barco_submarino = Barco('submarino', (320, 550), self.cuadricula)
        self.barco_acorazado = Barco('acorazado', (110, 590), self.cuadricula)
        self.barco_portaviones = Barco('portaviones', (260, 590), self.cuadricula)
        self.flota = [self.barco_destructor, self.barco_crucero, self.barco_submarino, self.barco_acorazado,
                      self.barco_portaviones]
        self.barcos_estan_colocados = False

        self.indices_flota = []
        self.mapa_enemigo = ["Desconocido" for i in range(100)]

        self.imagen_explosion = pygame.image.load('Imagenes/imagen_explosion.png').convert_alpha()
        self.imagen_explosion = pygame.transform.scale(self.imagen_explosion, (self.cuadricula.MEDIDA_CELDA[0],
                                                                               self.cuadricula.MEDIDA_CELDA[1]))

    def computar_indices_flota(self):
        for ship in self.flota:
            ship.computar_indices()
            for indice in ship.indices:
                self.indices_flota.append(indice)

    def dibujar_disparos(self, oponente):
        colores_disparos = {"Agua": AZUL, "Tocado": ROJO}

        for indice in range(100):
            x_centro_disparo = \
                oponente.cuadricula.IZQUIERDA_CUADRICULA + indice % 10 * oponente.cuadricula.MEDIDA_CELDA[1] \
                + oponente.cuadricula.MEDIDA_CELDA[1] // 2
            y_centro_disparo = \
                oponente.cuadricula.ARRIBA_CUADRICULA + indice // 10 * oponente.cuadricula.MEDIDA_CELDA[0] \
                + oponente.cuadricula.MEDIDA_CELDA[1] // 2

            if self.mapa_enemigo[indice] == "Agua":
                pygame.draw.circle(ventana, colores_disparos[self.mapa_enemigo[indice]],
                                   (x_centro_disparo, y_centro_disparo),
                                   radius=oponente.cuadricula.MEDIDA_CELDA[1] // 4)

            elif self.mapa_enemigo[indice] == "Tocado":
                if oponente == self.juego_principal.jugador_virtual:
                    pygame.draw.circle(ventana, colores_disparos[self.mapa_enemigo[indice]],
                                       (x_centro_disparo, y_centro_disparo),
                                       radius=oponente.cuadricula.MEDIDA_CELDA[1] // 4)

                elif oponente == self.juego_principal.jugador_humano:
                    imagen_explosion_rect = self.imagen_explosion.get_rect(center=(x_centro_disparo, y_centro_disparo))
                    ventana.blit(self.imagen_explosion, imagen_explosion_rect)

            elif self.mapa_enemigo[indice] == "Hundido":
                imagen_explosion_rect = self.imagen_explosion.get_rect(center=(x_centro_disparo, y_centro_disparo))
                ventana.blit(self.imagen_explosion, imagen_explosion_rect)


class JugadorHumano(Jugador):
    def __init__(self, juego_principal, origen_cuadricula):
        Jugador.__init__(self, juego_principal, origen_cuadricula)

    def colocar_barcos(self):
        moviendo_barco = False
        barco_que_movemos = None
        clock = pygame.time.Clock()
        while not self.barcos_estan_colocados:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Seleccionar el barco que vamos a mover con el cursor del raton
                elif event.type == MOUSEBUTTONDOWN:
                    for barco in self.flota:
                        if barco.rect.collidepoint(event.pos):
                            barco_que_movemos = barco
                            moviendo_barco = True

                # Colocar el barco soltando el boton del raton. Si no se coloca el barco dentro de la cuadrícula, este
                # volverá a su posición inicial automaticamente
                elif event.type == MOUSEBUTTONUP and moviendo_barco:
                    if (barco_que_movemos.rect.left + 15) < self.cuadricula.IZQUIERDA_CUADRICULA or \
                       (barco_que_movemos.rect.right - 15) >= self.cuadricula.DERECHA_CUADRICULA or \
                       (barco_que_movemos.rect.top + 15) < self.cuadricula.ARRIBA_CUADRICULA or \
                       (barco_que_movemos.rect.bottom - 15) >= self.cuadricula.ABAJO_CUADRICULA:
                        barco_que_movemos.rect.topleft = barco_que_movemos.posicion_inicial
                        if barco_que_movemos.direccion == 'vertical':
                            barco_que_movemos.girar_barco()
                    else:
                        barco_que_movemos.rect.topleft = (
                            self.cuadricula.pos_cuadricula_a_pos_pantalla(self.cuadricula.obtener_pos_cuadricula(
                                (barco_que_movemos.rect.topleft[0] + 15, barco_que_movemos.rect.topleft[1] + 15))))

                        for barco in self.flota:
                            if barco is not barco_que_movemos and barco_que_movemos.rect.colliderect(barco.rect):
                                barco_que_movemos.rect.topleft = barco_que_movemos.posicion_inicial
                                if barco_que_movemos.direccion == 'vertical':
                                    barco_que_movemos.girar_barco()
                                break

                    moviendo_barco = False

                # Mover el barco con el cursor del raton
                elif event.type == MOUSEMOTION and moviendo_barco:
                    barco_que_movemos.rect.move_ip(event.rel)

                # Mientras tenemos un barco seleccionado, podemos pulsar la tecla R para girar el barco.
                elif event.type == pygame.KEYDOWN and moviendo_barco:
                    if event.key == pygame.K_r:
                        barco_que_movemos.girar_barco()

                # Una vez tengamos todos los barcos colocados, pulsando la tecla Intro empezar la partida.
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        for barco in self.flota:
                            if barco.rect.topleft == barco.posicion_inicial:
                                break
                            else:
                                self.barcos_estan_colocados = True

            self.juego_principal.mostrar_elementos(barco_que_movemos)

            pygame.display.update()
            clock.tick(60)


class JugadorVirtual(Jugador):
    def __init__(self, juego_principal, start_grid):
        self.tiempo_disparo = 10  # milisegundos
        Jugador.__init__(self, juego_principal, start_grid)
        for barco in self.flota:
            barco.ocultado = True

    def colocar_barcos(self):
        for barco_que_colocamos in self.flota:
            barco_colocado = False
            while not barco_colocado:
                barco_que_colocamos.rect.topleft = (self.cuadricula.IZQUIERDA_CUADRICULA + random.randint(0, 9)
                                                    * self.cuadricula.MEDIDA_CELDA[0],
                                                    self.cuadricula.ARRIBA_CUADRICULA + random.randint(0, 9)
                                                    * self.cuadricula.MEDIDA_CELDA[1])
                if random.randint(0, 1) == 1:
                    barco_que_colocamos.girar_barco()
                if self.cuadricula.superficie_rect.contains(barco_que_colocamos.rect):
                    for barco in self.flota:
                        if barco is not barco_que_colocamos \
                                and barco.rect.colliderect(barco_que_colocamos.rect):
                            barco_colocado = False
                            break
                        barco_colocado = True

    def disparar(self):
        desconocidos = [indice for indice, celda in enumerate(self.mapa_enemigo) if celda == "Desconocido"]
        tocados = [indice for indice, celda in enumerate(self.mapa_enemigo) if celda == "Tocado"]

        # Creamos una lista con los indices de las celdas de tipo "Desconocido"
        # que tengan una celda vecina de tipo "Tocado".
        desconocidos_con_vecinos_tocados1 = []
        # Creamos una segunda lista con los indices de las celdas de tipo "Desconocido"
        # que tengan una celda vecina segunda de tipo "Tocado".
        desconocidos_con_vecinos_tocados2 = []
        for d in desconocidos:
            if (d + 1 in tocados and (d + 1) // 10 == d // 10) or\
               (d - 1 in tocados and (d - 1) // 10 == d // 10) or \
                    d-10 in tocados or d+10 in tocados:
                desconocidos_con_vecinos_tocados1.append(d)

            if (d + 2 in tocados and (d + 2) // 10 == d // 10) or\
               (d - 2 in tocados and (d - 2) // 10 == d // 10) or\
                    d - 20 in tocados or d + 20 in tocados:
                desconocidos_con_vecinos_tocados2.append(d)
        # Cuando buscamos los vecinos (d +- 1) o (d +- 2) estamos buscando en la dirección horizontal, mientras que si
        # buscamos los vecinos (d +- 10) o (d +- 20)  estamos buscando en la dirección vertical. Cuando  buscamos en la
        # dirección horizontal tenemos que tener en cuenta que los indices (d +- 1) y (d +- 2) no pertenezcan a otra
        # fila. Esto lo hacemos comprobando la división entera por 10. Por ejemplo, si miramos la posición d = 9,
        # estamos al final de la primera fila de la cuadrícula,por tanto, d+1 y d+2 serían las posiciones del las dos
        # primeras celdas de la segunda fila, y como un barco no puede estar partido en dos, estos puntos no se tienen
        # que considerar vecinos.

        # Si tenemos dos celdas consecutivas de tipo "Tocado" quiere decir que en esa dirección hay un barco.
        for d in desconocidos:
            if d in desconocidos_con_vecinos_tocados1 and d in desconocidos_con_vecinos_tocados2:
                self.juego_principal.actualizar_jugada(d)
                return

        # Si no tenemos dos celdas consecutivas de tipo "Tocado" pero tenemos una, dispararemos en una celda vecina.
        if len(desconocidos_con_vecinos_tocados1) > 0:
            self.juego_principal.actualizar_jugada(random.choice(desconocidos_con_vecinos_tocados1))
            return

        # Si no tenemos ninguna celda de tipo "Tocado" dispararemos siguiendo un patron que nos permita encontrar hasta
        # el barco mas pequeño sin desperdiciar disparos. Como sabemos que el barco más pequeño es de dos celdas,
        # dispararemos solo en las celdas pares, así cubriremos toda la cuadrícula dejando solo un espacio libre entre
        # dos disparos. El patron de disparos se asemejará a un tablero de ajedrez.
        tablero_ajedrez = []
        for d in desconocidos:
            row = d // 10
            col = d % 10
            if (row + col) % 2 == 0:
                tablero_ajedrez.append(d)
        if len(tablero_ajedrez) > 0:
            self.juego_principal.actualizar_jugada(random.choice(tablero_ajedrez))
            return

        # movimiento random
        # if len(desconocidos) > 0:
        #     random_index = random.choice(desconocidos)
        #     self.juego_principal.actualizar_jugada(random_index)


class Barco:
    def __init__(self, tipo_barco, posicion_inicial, cuadricula, ocultado=False):
        self.tipo_barco = tipo_barco
        self.cuadricula = cuadricula
        self.tipo_barco = tipo_barco
        self.posicion_inicial = posicion_inicial
        self.ocultado = ocultado
        self.direccion = 'horizontal'

        if tipo_barco == "destructor":
            self.largo = 2
        elif tipo_barco == "crucero":
            self.largo = 3
        elif tipo_barco == "submarino":
            self.largo = 3
        elif tipo_barco == "acorazado":
            self.largo = 4
        elif tipo_barco == "portaviones":
            self.largo = 5

        self.imagen_barco = pygame.image.load('Imagenes/' + tipo_barco + '.png').convert_alpha()
        self.imagen_barco = pygame.transform.scale(self.imagen_barco, (self.cuadricula.MEDIDA_CELDA[0] * self.largo,
                                                                       self.cuadricula.MEDIDA_CELDA[1]))
        self.rect = self.imagen_barco.get_rect(topleft=self.posicion_inicial)

        self.indices = []

    def computar_indices(self):
        coordenadas = self.cuadricula.obtener_pos_cuadricula((self.rect.topleft[0], self.rect.topleft[1]))
        primer_indice = coordenadas[1] * 10 + coordenadas[0]
        if self.direccion == 'horizontal':
            self.indices = [primer_indice + i for i in range(self.largo)]
        elif self.direccion == 'vertical':
            self.indices = [primer_indice + i * 10 for i in range(self.largo)]

    def mostrar_barco(self):
        if self.ocultado:
            return
        ventana.blit(self.imagen_barco, self.rect)

    def girar_barco(self):
        if self.direccion == 'horizontal':
            self.imagen_barco = pygame.transform.rotate(self.imagen_barco, -90)
            self.rect = self.imagen_barco.get_rect(
                topleft=self.rect.topleft)
            self.direccion = 'vertical'
        elif self.direccion == 'vertical':
            self.imagen_barco = pygame.transform.rotate(self.imagen_barco, 90)
            self.rect = self.imagen_barco.get_rect(
                topleft=self.rect.topleft)
            self.direccion = 'horizontal'


class BotonPrincipal:
    def __init__(self, imagen, posicion, entrada_texto, fuente, color_texto, color_flotante_texto, ancho, alto,
                 ancho_borde, radio_borde):
        self.imagen = imagen
        self.posicion_x = posicion[0]
        self.posicion_y = posicion[1]
        self.fuente = fuente
        self.color_base, self.color_flotante_texto, self.color_borde = color_texto, color_flotante_texto, (0, 0, 0)
        self.ancho = ancho
        self.alto = alto
        self.ancho_borde = ancho_borde
        self.radio_borde = radio_borde
        self.entrada_texto = entrada_texto
        self.texto = self.fuente.render(self.entrada_texto, True, self.color_base)
        if self.imagen is None:
            self.superficie = pygame.Surface((self.ancho, self.alto))
            self.rect = self.superficie.get_rect(center=(self.posicion_x, self.posicion_y))
        else:
            self.rect = self.imagen.get_rect(center=(self.posicion_x, self.posicion_y))
        self.rect_texto = self.texto.get_rect(center=(self.posicion_x, self.posicion_y))

    def mostrar(self, ventana):
        if self.imagen is None:
            pygame.draw.rect(ventana, BLANCO, self.rect, 0, self.radio_borde)
            if self.ancho_borde > 0:
                pygame.draw.rect(ventana, self.color_borde, self.rect, self.ancho_borde, self.radio_borde)
        else:
            ventana.blit(self.imagen, self.rect)
        ventana.blit(self.texto, self.rect_texto)

    def raton_encima(self, posicion_raton):
        if posicion_raton[0] in range(self.rect.left, self.rect.right) and posicion_raton[1] in range(self.rect.top,
                                                                                                      self.rect.bottom):
            return True
        return False

    def cambiar_color(self, posicion_raton):
        if self.raton_encima(posicion_raton):
            self.texto = self.fuente.render(self.entrada_texto, True, self.color_flotante_texto)
            self.color_borde = self.color_flotante_texto
        else:
            self.texto = self.fuente.render(self.entrada_texto, True, self.color_base)
            self.color_borde = (0, 0, 0)


if __name__ == '__main__':
    juego = JuegoHundirFlota()
    juego.ejecutar()
