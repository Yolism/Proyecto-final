import pygame
import sys
import os
import capa2logica
import capa3verificacion

def obtener_ultimo_score():
    # Lee el último score guardado 
    if os.path.exists("score_record.txt"):
        with open("score_record.txt", "r") as f:
            try:
                return int(f.read().strip())
            except:
                return 0
    return 0

def guardar_ultimo_score(nuevo_score):
    # Guarda el score si superó o actualizó el registro
    with open("score_record.txt", "w") as f:
        f.write(str(nuevo_score))

def iniciar_juego():
    pygame.init()
    
    ANCHO, ALTO = 600, 400
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Juego de la Serpiente 🐍")
    reloj = pygame.time.Clock()
    
    # Fuentes para los menús y textos
    fuente_titulo = pygame.font.SysFont("Comic Sans MS", 35, bold=True)
    fuente_menu = pygame.font.SysFont("Comic Sans MS", 24)
    fuente_hud = pygame.font.SysFont("Comic Sans MS", 20)
    
    # Cargar récord histórico
    ultimo_score_registrado = obtener_ultimo_score()
    
    # ESTADO INICIAL: PANTALLA PRINCIPAL
    en_menu_principal = True
    juego_continua = False
    
    # ==========================================
    # INICIA EL MENÚ PRINCIPAL (PÁGINA DE INICIO)
    # ==========================================
    while en_menu_principal:
        pantalla.fill((15, 15, 30)) # Fondo azul oscuro para el menú
        
        # Renderizar textos propuestos
        txt_titulo = fuente_titulo.render("MENU PRINCIPAL", True, (255, 255, 255))
        txt_partida = fuente_menu.render("> Presiona [ ENTER ] para Nueva Partida", True, (0, 255, 0))
        txt_record = fuente_menu.render(f"Último Score Registrado: {ultimo_score_registrado}", True, (255, 215, 0))
        txt_salir = fuente_hud.render("Presiona [ ESC ] para Salir", True, (200, 200, 200))
        
        # Posicionar textos s
        pantalla.blit(txt_titulo, (ANCHO // 2 - txt_titulo.get_width() // 2, 80))
        pantalla.blit(txt_record, (ANCHO // 2 - txt_record.get_width() // 2, 160))
        pantalla.blit(txt_partida, (ANCHO // 2 - txt_partida.get_width() // 2, 240))
        pantalla.blit(txt_salir, (ANCHO // 2 - txt_salir.get_width() // 2, 330))
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: # ENTER inicia Partida Nueva
                    en_menu_principal = False
                    juego_continua = True
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        reloj.tick(15)

    # ==========================================
    # CONFIGURACIÓN DE PARTIDA NUEVA
    # ==========================================
    direccion_actual = "DERECHA"
    cuerpo_serpiente = [(100, 100), (80, 100), (60, 100)]
    fruta_x, fruta_y = 300, 200
    score = 0
    tiempo_inicial = pygame.time.get_ticks()
    
    # ==========================================
    # CICLO DEL JUEGO ACTIVO
    # ==========================================
    while juego_continua:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                juego_continua = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and direccion_actual != "ABAJO":
                    direccion_actual = "ARRIBA"
                elif evento.key == pygame.K_DOWN and direccion_actual != "ARRIBA":
                    direccion_actual = "ABAJO"
                elif evento.key == pygame.K_LEFT and direccion_actual != "DERECHA":
                    direccion_actual = "IZQUIERDA"
                elif evento.key == pygame.K_RIGHT and direccion_actual != "IZQUIERDA":
                    direccion_actual = "DERECHA"

        # Capa 2: Lógica de Movimiento
        cuerpo_serpiente = capa2logica.mover_serpiente(cuerpo_serpiente, direccion_actual)
        cabeza_x, cabeza_y = cuerpo_serpiente[0]
        
        # Capa 3: Verificación de Comida
        if capa3verificacion.comprobar_comida(cabeza_x, cabeza_y, fruta_x, fruta_y):
            score += 10
            fruta_x, fruta_y = capa3verificacion.generar_nueva_fruta(ANCHO, ALTO)
        else:
            cuerpo_serpiente.pop()
            
        # Capa 3: Verificación de Colisiones
        if capa3verificacion.comprobar_colision(cabeza_x, cabeza_y, ANCHO, ALTO, cuerpo_serpiente):
            juego_continua = False

        # Dibujar Interfaz del juego (Fondo negro en partida activa)
        pantalla.fill((0, 0, 0))
        
        # Dibujar Manzana y Cuerpo
        pygame.draw.rect(pantalla, (255, 255, 0), (fruta_x, fruta_y, 20, 20))
        for segmento in cuerpo_serpiente:
            pygame.draw.rect(pantalla, (255, 255, 255), (segmento[0], segmento[1], 20, 20))
            
        # Calcular e imprimir Score, Tiempo y Récord en el HUD
        tiempo_actual = (pygame.time.get_ticks() - tiempo_inicial) // 1000
        texto_score = fuente_hud.render(f"Score: {score}", True, (0, 255, 0))
        texto_record_hud = fuente_hud.render(f"Top: {ultimo_score_registrado}", True, (255, 215, 0))
        texto_tiempo = fuente_hud.render(f"Tiempo: {tiempo_actual}s", True, (255, 255, 0))
        
        pantalla.blit(texto_score, (10, 10))
        pantalla.blit(texto_record_hud, (ANCHO // 2 - 30, 10))
        pantalla.blit(texto_tiempo, (ANCHO - 120, 10))
        
        pygame.display.flip()
        reloj.tick(6) # Velocidad moderada y controlable

    # Al perder, actualizar el registro si el score actual es el más alto
    if score > ultimo_score_registrado:
        guardar_ultimo_score(score)
    else:
        guardar_ultimo_score(ultimo_score_registrado)

    print(f"GAME OVER: Tu puntaje fue {score}")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    iniciar_juego()
