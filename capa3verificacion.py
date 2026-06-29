# capa3verificacion.py
import random

def comprobar_colision(pos_x, pos_y, ancho_pantalla, alto_pantalla, cuerpo_serpiente):
    # Colisión con los bordes de la ventana
    if pos_x < 0 or pos_x >= ancho_pantalla or pos_y < 0 or pos_y >= alto_pantalla:
        return True
    
    # Colisión con su propio cuerpo
    if (pos_x, pos_y) in cuerpo_serpiente[1:]:
        return True
        
    return False

def comprobar_comida(cabeza_x, cabeza_y, fruta_x, fruta_y):
    if cabeza_x == fruta_x and cabeza_y == fruta_y:
        return True
    return False

def generar_nueva_fruta(ancho, alto):
    x = random.randint(0, (ancho - 20) // 20) * 20
    y = random.randint(0, (alto - 20) // 20) * 20
    return x, y
