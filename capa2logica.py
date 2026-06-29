# capa2logica.py

def mover_serpiente(cuerpo_serpiente, direccion):
    velocidad = 20
    cabeza_x, cabeza_y = cuerpo_serpiente[0]
    
    if direccion == "DERECHA":
        cabeza_x += velocidad
    elif direccion == "IZQUIERDA":
        cabeza_x -= velocidad
    elif direccion == "ARRIBA":
        cabeza_y -= velocidad
    elif direccion == "ABAJO":
        cabeza_y += velocidad
        
    # Insertar la nueva posición de la cabeza al principio de la lista
    cuerpo_serpiente.insert(0, (cabeza_x, cabeza_y))
    return cuerpo_serpiente
