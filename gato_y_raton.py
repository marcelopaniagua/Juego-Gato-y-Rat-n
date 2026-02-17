
import random
import copy

#Configuracion

FILAS = 8
COLUMNAS = 8
MAX_PROFUNDIDAD = 3
MAX_TURNOS = 35

MOVIMIENTOS = {
    "w": (-1, 0), #arriba
    "s": (1, 0), #abajo
    "a": (0, -1), #izquierda
    "d": (0, 1) # derecha
}

#Estado Inicial

def creacion_estado_inicial():
    return{
        "gato": (0, 0),
        "raton": (FILAS -1, COLUMNAS -1),
        "turno": "raton",
        "turnos": 0
    }

# Tablero

def creacion_tablero_vacio():
    return[["." for _ in range(COLUMNAS)] for _ in range(FILAS)]

def construccion_tablero_del_estado(estado):
    tablero = creacion_tablero_vacio()
    gx, gy = estado ["gato"]
    rx, ry = estado ["raton"]
    tablero[gx][gy] = "G"
    tablero[rx][ry] = "R"
    return tablero 

def print_tablero(estado):
    tablero = construccion_tablero_del_estado(estado)
    print("_" * (COLUMNAS * 2))
    for fila in tablero:
        print(" ".join(fila))
    print("-" * (COLUMNAS * 2))
    print()

# Movientoss

def es_una_posicion_valida(pos):
    x, y = pos
    return 0 <= x < FILAS and 0 <= y < COLUMNAS

def mover_posicion(posicion, key):
    if key not in MOVIMIENTOS:
        return posicion
    
    dx, dy = MOVIMIENTOS[key]
    nueva_pos = (posicion[0] + dx, posicion[1] + dy)

    if es_una_posicion_valida(nueva_pos):
        return nueva_pos
    
    return posicion 

def obtener_posibles_mov(posicion):
    movientos = []
    for dx, dy in MOVIMIENTOS.values():
        nueva_pos = (posicion[0] + dx, posicion[1] + dy)
        if es_una_posicion_valida(nueva_pos):
            movientos.append(nueva_pos)
    return movientos

# FINAL DEL JUEGO!! 

def es_terminal(estado):
    if estado["gato"] == estado["raton"]:
        return True
    if estado["turnos"] >= MAX_TURNOS:
        return True
    return False

# EVALUACION

def evalucion_estado(estado):
    gx, gy = estado ["gato"]
    rx, ry = estado ["raton"]
    return abs (gx - rx) + abs (gy - ry)

# MINIMAX (IA) 

def minimax(estado, profundida, es_maximizar):
    if es_terminal(estado) or profundida == 0:
        return evalucion_estado(estado)
    
    if es_maximizar:  #RATON 
        mejor = -float("inf")
        for mov in obtener_posibles_mov(estado["raton"]):
            nuevo_estado = copy.deepcopy(estado)
            nuevo_estado["raton"] = mov
            nuevo_estado["turno"] = "gato"
            nuevo_estado["turnos"] += 1
            mejor = max(mejor, minimax(nuevo_estado, profundida - 1, False))
        return mejor
    else: #GATO
        mejor = float("inf")
        for mov in obtener_posibles_mov(estado["gato"]):
            nuevo_estado = copy.deepcopy(estado)
            nuevo_estado["gato"] = mov
            nuevo_estado["turno"] = "raton"
            nuevo_estado["turnos"] += 1
            mejor = min(mejor, minimax(nuevo_estado, profundida - 1, True))
        return mejor
    
def mejor_movimiento_ia(estado, ia_player):
    if ia_player == "raton":
        mejor_valor = -float("inf")
        mejor_movimiento = estado["raton"]
        for mov in obtener_posibles_mov(estado["raton"]):
            nuevo_estado = copy.deepcopy(estado)
            nuevo_estado["raton"] = mov
            nuevo_estado["turno"] = "gato"
            nuevo_estado["turnos"] += 1
            valor = minimax(nuevo_estado, MAX_PROFUNDIDAD, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
        return mejor_movimiento
    
    else: # GATO
        mejor_valor = float("inf")
        mejor_movimiento = estado["gato"]
        for mov in obtener_posibles_mov(estado["gato"]):
            nuevo_estado = copy.deepcopy(estado)
            nuevo_estado["gato"] = mov
            nuevo_estado["turno"] = "raton"
            valor = minimax(nuevo_estado, MAX_PROFUNDIDAD, True)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
        return mejor_movimiento
    
# JUEGO PRINCIPAL

def play_game():
    estado = creacion_estado_inicial()

    print("🐭🐱 LABERINTO DEL GATO Y EL RATON 🐭🐱")
    eleccion = input("queres ser raton (r) o gato (g)? ").lower()
    jugador = "raton" if eleccion == "r" else "gato"
    jugador_ia = "gato" if jugador == "raton" else "raton"

    while not es_terminal(estado):
        print_tablero(estado)
        print(f"Turno{estado['turnos']} - Juega: {estado['turno']}")

        if estado["turno"] == jugador:
            key = input("Mover (w/a/s/d): ").lower()
            if jugador == "raton":
                 estado["raton"] = mover_posicion(estado["raton"], key)
            else:
                estado["gato"] = mover_posicion(estado["gato"], key)
            estado["turno"] = jugador_ia
            estado["turnos"] += 1
        else:
            print("🤖 La IA está pensando...")
            mov = mejor_movimiento_ia(estado, jugador_ia)
            if jugador_ia == "raton":
                estado["raton"] = mov
            else:
                estado["gato"] = mov
            estado["turnos"] += 1
            estado["turno"] = jugador


    print_tablero(estado)
    if estado["gato"] == estado["raton"]:
        print("🐱 El gato atrapó al ratón")
    else:
        print("🐭 El ratón sobrevivió")

# MAIN
if __name__ == "__main__":
    play_game()