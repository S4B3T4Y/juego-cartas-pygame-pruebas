import pygame
import random
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 900, 650
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Cartas - Batalla de Fuerzas")

# Configuración visual mejorada
COLORES = {
    "fondo": (30, 30, 40),
    "texto": (240, 240, 240),
    "jugador": (70, 130, 200),
    "cpu": (200, 70, 100),
    "seleccion": (100, 200, 100),
    "borde": (180, 160, 100),
    "btn": (80, 80, 100),
    "btn_hover": (110, 110, 130)
}

FUENTE_NORMAL = pygame.font.SysFont("Arial", 26, bold=True)
FUENTE_GRANDE = pygame.font.SysFont("Arial", 42, bold=True)
FUENTE_CARTA = pygame.font.SysFont("Arial", 22, bold=True)

# Funciones para cartas
def crear_carta(nombre, fuerza, bonus=0):
    """Crea una carta como diccionario"""
    return {"nombre": nombre, "fuerza": fuerza, "bonus": bonus}

def fuerza_total(carta):
    """Calcula la fuerza total de una carta"""
    return carta["fuerza"] + carta["bonus"]

def texto_carta(carta):
    """Devuelve el texto para mostrar la carta"""
    return f"{carta['nombre']} (F:{carta['fuerza']}+{carta['bonus']})"

# Funciones del juego
def crear_mazo():
    """Crea y baraja un mazo de cartas"""
    tipos = ["Guerrero", "Mago", "Arquero", "Dragón", "Caballero", "Hechicera", "Titán", "Bestia"]
    mazo = []
    for tipo in tipos:
        for _ in range(3):
            mazo.append(crear_carta(tipo, random.randint(1, 10), random.randint(0, 3)))
    random.shuffle(mazo)
    return mazo

def repartir_cartas(mazo, cantidad):
    """Reparte cartas del mazo"""
    return [mazo.pop(0) for _ in range(cantidad)] if len(mazo) >= cantidad else mazo.copy()

# Funciones visuales mejoradas
def dibujar_fondo():
    """Dibuja un fondo con degradado"""
    for i in range(ALTO):
        color = (max(10, 30 - i//30), max(10, 30 - i//30), max(20, 40 - i//30))
        pygame.draw.line(VENTANA, color, (0, i), (ANCHO, i))
    # Barra superior e inferior
    pygame.draw.rect(VENTANA, (40, 40, 60), (0, 0, ANCHO, 80))
    pygame.draw.rect(VENTANA, (20, 20, 30), (0, ALTO-100, ANCHO, 100))

def dibujar_carta(x, y, carta, seleccionada=False, es_cpu=False):
    """Dibuja una carta con mejor aspecto visual"""
    color_fondo = COLORES["cpu"] if es_cpu else COLORES["jugador"]
    if seleccionada:
        color_fondo = COLORES["seleccion"]
    
    # Borde de la carta
    pygame.draw.rect(VENTANA, COLORES["borde"], (x-3, y-3, 146, 96), border_radius=8)
    # Cuerpo de la carta
    pygame.draw.rect(VENTANA, color_fondo, (x, y, 140, 90), border_radius=6)
    
    # Nombre de la carta
    nombre = FUENTE_CARTA.render(carta["nombre"], True, COLORES["texto"])
    VENTANA.blit(nombre, (x + 10, y + 10))
    
    # Estadísticas
    fuerza = FUENTE_NORMAL.render(f"Fuerza: {carta['fuerza']}", True, COLORES["texto"])
    bonus = FUENTE_NORMAL.render(f"Bonus: +{carta['bonus']}", True, COLORES["texto"])
    total = FUENTE_NORMAL.render(f"Total: {fuerza_total(carta)}", True, COLORES["texto"])
    
    VENTANA.blit(fuerza, (x + 10, y + 35))
    VENTANA.blit(bonus, (x + 10, y + 55))
    VENTANA.blit(total, (x + 10, y + 75))

def dibujar_boton(x, y, ancho, alto, texto):
    """Dibuja un botón con efecto hover"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover = (x <= mouse_x <= x + ancho and y <= mouse_y <= y + alto)
    
    color = COLORES["btn_hover"] if hover else COLORES["btn"]
    pygame.draw.rect(VENTANA, color, (x, y, ancho, alto), border_radius=8)
    pygame.draw.rect(VENTANA, COLORES["texto"], (x, y, ancho, alto), 2, border_radius=8)
    
    texto_btn = FUENTE_NORMAL.render(texto, True, COLORES["texto"])
    VENTANA.blit(texto_btn, (x + ancho//2 - texto_btn.get_width()//2, 
                            y + alto//2 - texto_btn.get_height()//2))
    return hover

def mostrar_mensaje(texto, y=250, fuente=FUENTE_GRANDE, color=COLORES["texto"]):
    """Muestra un mensaje centrado en pantalla"""
    texto_render = fuente.render(texto, True, color)
    VENTANA.blit(texto_render, (ANCHO//2 - texto_render.get_width()//2, y))

# Función principal del juego
def jugar():
    """Controla el flujo principal del juego"""
    mazo_jugador = crear_mazo()
    mazo_cpu = crear_mazo()
    
    mano_jugador = repartir_cartas(mazo_jugador, 5)
    mano_cpu = repartir_cartas(mazo_cpu, 5)
    
    seleccion = -1
    turno = 1
    mensaje = ""
    carta_jugada_cpu = None
    puntaje = [0, 0]  # [jugador, cpu]
    
    while True:
        # Dibujado
        dibujar_fondo()
        
        # Título
        titulo = FUENTE_GRANDE.render("Batalla de Cartas", True, COLORES["texto"])
        VENTANA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 20))
        
        # Marcador
        marcador = FUENTE_NORMAL.render(f"Jugador: {puntaje[0]}  -  CPU: {puntaje[1]}", 
                                      True, COLORES["texto"])
        VENTANA.blit(marcador, (ANCHO//2 - marcador.get_width()//2, 70))
        
        # Turno actual
        texto_turno = FUENTE_NORMAL.render(f"Turno: {turno}", True, COLORES["texto"])
        VENTANA.blit(texto_turno, (ANCHO - 150, 70))
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verificar clic en cartas del jugador
                for i in range(len(mano_jugador)):
                    carta_x = 50 + i * 160
                    carta_y = 450
                    if carta_x <= mouse_x <= carta_x + 140 and carta_y <= mouse_y <= carta_y + 90:
                        seleccion = i
        
        # Lógica del turno
        if seleccion != -1 and mensaje == "" and 0 <= seleccion < len(mano_jugador):
            carta_jugador = mano_jugador.pop(seleccion)
            
            if mano_cpu:  # Asegurar que la CPU tenga cartas
                carta_cpu = min(mano_cpu, key=fuerza_total)
                mano_cpu.remove(carta_cpu)
                carta_jugada_cpu = carta_cpu
                
                # Comparar fuerzas
                if fuerza_total(carta_jugador) > fuerza_total(carta_cpu):
                    mensaje = "¡Ganaste este turno!"
                    puntaje[0] += 1
                elif fuerza_total(carta_jugador) < fuerza_total(carta_cpu):
                    mensaje = "La CPU ganó este turno"
                    puntaje[1] += 1
                else:
                    mensaje = "¡Empate!"
                
                # Reponer cartas
                if mazo_jugador and len(mano_jugador) < 5:
                    mano_jugador.append(mazo_jugador.pop(0))
                if mazo_cpu and len(mano_cpu) < 5:
                    mano_cpu.append(mazo_cpu.pop(0))
                
                turno += 1
                seleccion = -1
        
        # Cartas CPU
        texto_cpu = FUENTE_NORMAL.render("Cartas de la CPU:", True, COLORES["texto"])
        VENTANA.blit(texto_cpu, (50, 120))
        for i, carta in enumerate(mano_cpu):
            dibujar_carta(50 + i * 160, 150, carta, False, True)
        
        # Cartas jugador
        texto_jugador = FUENTE_NORMAL.render("Tus cartas:", True, COLORES["texto"])
        VENTANA.blit(texto_jugador, (50, 420))
        for i, carta in enumerate(mano_jugador):
            dibujar_carta(50 + i * 160, 450, carta, i == seleccion)
        
        # Carta jugada por CPU
        if carta_jugada_cpu:
            texto_cpu_jugada = FUENTE_NORMAL.render(
                f"La CPU jugó: {carta_jugada_cpu['nombre']} (Total: {fuerza_total(carta_jugada_cpu)})", 
                True, COLORES["texto"])
            VENTANA.blit(texto_cpu_jugada, (50, 380))
        
        # Mensaje y botón continuar
        if mensaje:
            color_mensaje = COLORES["jugador"] if "Ganaste" in mensaje else \
                           COLORES["cpu"] if "CPU" in mensaje else \
                           COLORES["texto"]
            mostrar_mensaje(mensaje, 300, FUENTE_GRANDE, color_mensaje)
            
            if dibujar_boton(ANCHO//2 - 100, 350, 200, 50, "Continuar"):
                if pygame.mouse.get_pressed()[0]:
                    mensaje = ""
                    carta_jugada_cpu = None
        
        # Fin del juego
        if not mano_jugador or not mano_cpu:
            if puntaje[0] > puntaje[1]:
                resultado = "¡Ganaste la partida! 🎉"
                color_resultado = COLORES["jugador"]
            elif puntaje[0] < puntaje[1]:
                resultado = "¡La CPU ganó la partida!"
                color_resultado = COLORES["cpu"]
            else:
                resultado = "¡Empate final!"
                color_resultado = (200, 200, 100)
            
            mostrar_mensaje(resultado, 250, FUENTE_GRANDE, color_resultado)
            mostrar_mensaje(f"Marcador final: {puntaje[0]} - {puntaje[1]}", 300)
            
            if dibujar_boton(ANCHO//2 - 100, 350, 200, 50, "Jugar otra vez"):
                if pygame.mouse.get_pressed()[0]:
                    return jugar()  # Reinicia el juego
            
            if dibujar_boton(ANCHO//2 - 100, 420, 200, 50, "Salir"):
                if pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()
            pygame.time.delay(100)
            continue
        
        pygame.display.flip()

# Iniciar el juego
if __name__ == "__main__":
    jugar()