import pygame
import sys
from cartas import generar_carta_aleatoria

# Configuración de ventana
ANCHO, ALTO = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)

def inicializar_pygame():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Cartas vs CPU")
    return ventana

def crear_mano(faccion, cantidad=5):
    return [generar_carta_aleatoria(faccion) for _ in range(cantidad)]

def dibujar_mano(ventana, mano, y_pos, fuente):
    for i, (nombre, valor) in enumerate(mano):
        pygame.draw.rect(ventana, WHITE, (50 + i*150, y_pos, 120, 100))
        texto = fuente.render(f"{nombre} ({valor})", True, BLACK)
        ventana.blit(texto, (60 + i*150, y_pos + 35))

def turno(jugador, cpu):
    carta_jugador = jugador.pop(0)
    carta_cpu = cpu.pop(0)
    
    if carta_jugador[1] > carta_cpu[1]:
        resultado = "Ganaste el turno"
    elif carta_jugador[1] < carta_cpu[1]:
        resultado = "Perdiste el turno"
    else:
        resultado = "Empate"
    
    return carta_jugador, carta_cpu, resultado

def main():
    ventana = inicializar_pygame()
    fuente = pygame.font.SysFont("arial", 24)
    reloj = pygame.time.Clock()

    jugador = crear_mano("Reinos del Norte")
    cpu = crear_mano("Monstruos")

    resultado = ""
    carta_j, carta_c = None, None

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN and jugador and cpu:
                carta_j, carta_c, resultado = turno(jugador, cpu)

        ventana.fill(BLACK)
        dibujar_mano(ventana, jugador, 400, fuente)
        dibujar_mano(ventana, cpu, 100, fuente)

        if carta_j and carta_c:
            texto_j = fuente.render(f"Jugaste: {carta_j[0]} ({carta_j[1]})", True, WHITE)
            texto_c = fuente.render(f"CPU: {carta_c[0]} ({carta_c[1]})", True, WHITE)
            ventana.blit(texto_j, (50, 300))
            ventana.blit(texto_c, (50, 330))

        ventana.blit(fuente.render(resultado, True, GREEN), (50, 370))

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
