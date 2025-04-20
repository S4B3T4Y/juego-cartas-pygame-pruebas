import pygame
import random
import sys

pygame.init()

ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Cartas vs CPU")

FUENTE = pygame.font.SysFont("arial", 24)
GRANDE = pygame.font.SysFont("arial", 48)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
VERDE = (0, 180, 0)
GRIS = (100, 100, 100)

pygame.mixer.init()
sound_click = pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.Sound.get_raw(pygame.mixer.Sound(pygame.mixer.Sound.get_raw(pygame.mixer.Sound(b'\x00'))))))

class Carta:
    def __init__(self, nombre, potencia, potenciador=0):
        self.nombre = nombre
        self.potencia = potencia
        self.potenciador = potenciador

    def obtener_potencia_total(self):
        return self.potencia + self.potenciador

    def __str__(self):
        return f"{self.nombre} (Pot: {self.potencia}, +{self.potenciador})"

def crear_baraja():
    nombres = [
        "Guerrero", "Hechicera", "Arquero", "Bestia", "Ladrón", "Mago",
        "Paladín", "Dragón", "Asesino", "Titán", "Caballero", "Gólem"
    ]
    baraja = []
    for nombre in nombres:
        potencia = random.randint(3, 10)
        potenciador = random.randint(0, 2)
        baraja.append(Carta(nombre, potencia, potenciador))
    random.shuffle(baraja)
    return baraja

def dibujar_mano(mano, y, seleccionado=None):
    for i, carta in enumerate(mano):
        x = 20 + i * 160
        color = VERDE if i == seleccionado else BLANCO
        pygame.draw.rect(VENTANA, color, (x, y, 150, 100))
        texto = FUENTE.render(str(carta), True, NEGRO)
        VENTANA.blit(texto, (x + 5, y + 40))

def elegir_carta_cpu(mano):
    seleccion = min(mano, key=lambda c: c.obtener_potencia_total())
    mano.remove(seleccion)
    return seleccion

def menu():
    reloj = pygame.time.Clock()
    opciones = ["JUGAR", "INSTRUCCIONES", "CRÉDITOS", "SALIR"]
    seleccion = 0

    while True:
        VENTANA.fill(NEGRO)
        titulo = GRANDE.render("Juego de Cartas vs CPU", True, BLANCO)
        VENTANA.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 100))

        for i, opcion in enumerate(opciones):
            color = VERDE if i == seleccion else GRIS
            pygame.draw.rect(VENTANA, color, (ANCHO//2 - 150, 200 + i*70, 300, 50))
            texto = FUENTE.render(opcion, True, NEGRO)
            VENTANA.blit(texto, (ANCHO//2 - texto.get_width()//2, 215 + i*70))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    sound_click.play()
                    if opciones[seleccion] == "JUGAR":
                        return
                    elif opciones[seleccion] == "INSTRUCCIONES":
                        mostrar_instrucciones()
                    elif opciones[seleccion] == "CRÉDITOS":
                        mostrar_creditos()
                    elif opciones[seleccion] == "SALIR":
                        pygame.quit()
                        sys.exit()
        reloj.tick(30)

def mostrar_instrucciones():
    mostrar_texto(["Reglas del Juego:",
                  "- Se juega contra la CPU.",
                  "- Cada uno tiene un mazo de 12 cartas y recibe 4.",
                  "- Se juega una carta por turno.",
                  "- Gana la carta con más potencia.",
                  "- Se descuenta la potencia de la perdedora a la ganadora.",
                  "- Pierde quien se quede sin cartas.",
                  "Presiona cualquier tecla para volver al menú."])

def mostrar_creditos():
    mostrar_texto(["Créditos:", "Desarrollado por Franco Sabetay, Nahuel Kryc, Nacho lemarie, Juan Savedra.", "¡Gracias por jugar!", "Presiona cualquier tecla para volver al menú."])

def mostrar_texto(lineas):
    esperando = True
    while esperando:
        VENTANA.fill(NEGRO)
        for i, linea in enumerate(lineas):
            texto = FUENTE.render(linea, True, BLANCO)
            VENTANA.blit(texto, (ANCHO//2 - texto.get_width()//2, 100 + i*40))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                esperando = False


def main():
    menu()

    jugador = {"mazo": crear_baraja(), "mano": []}
    cpu = {"mazo": crear_baraja(), "mano": []}
    for _ in range(4):
        jugador["mano"].append(jugador["mazo"].pop(0))
        cpu["mano"].append(cpu["mazo"].pop(0))

    seleccion = None
    reloj = pygame.time.Clock()
    turno = 1
    resultado_turno = ""
    carta_cpu_actual = None

    corriendo = True
    while corriendo:
        VENTANA.fill(NEGRO)
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i in range(len(jugador["mano"])):
                    if 20 + i * 160 < mx < 170 + i * 160 and 450 < my < 550:
                        seleccion = i
                        sound_click.play()

        if seleccion is not None:
            carta_jugador = jugador["mano"].pop(seleccion)
            carta_cpu = elegir_carta_cpu(cpu["mano"])
            pot_j = carta_jugador.obtener_potencia_total()
            pot_c = carta_cpu.obtener_potencia_total()
            carta_cpu_actual = carta_cpu

            if pot_j > pot_c:
                carta_jugador.potencia -= pot_c
                resultado_turno = "Ganaste el turno"
                if carta_jugador.potencia > 0:
                    jugador["mano"].append(carta_jugador)
            elif pot_c > pot_j:
                carta_cpu.potencia -= pot_j
                resultado_turno = "CPU ganó el turno"
                if carta_cpu.potencia > 0:
                    cpu["mano"].append(carta_cpu)
            else:
                resultado_turno = "Empate"

            for p in [jugador, cpu]:
                if p["mazo"]:
                    p["mano"].append(p["mazo"].pop(0))

            seleccion = None
            turno += 1

        dibujar_mano(cpu["mano"], 50)
        dibujar_mano(jugador["mano"], 450, seleccion)

        texto_turno = FUENTE.render(f"Turno {turno}", True, BLANCO)
        VENTANA.blit(texto_turno, (ANCHO // 2 - 50, 10))

        if carta_cpu_actual:
            cpu_ult = FUENTE.render(f"CPU jugó: {str(carta_cpu_actual)}", True, BLANCO)
            VENTANA.blit(cpu_ult, (20, 370))

        resultado_texto = FUENTE.render(resultado_turno, True, BLANCO)
        VENTANA.blit(resultado_texto, (20, 400))

        if not jugador["mano"] or not cpu["mano"]:
            resultado_final = "Empate"
            if not jugador["mano"] and cpu["mano"]:
                resultado_final = "Perdiste"
            elif not cpu["mano"] and jugador["mano"]:
                resultado_final = "Ganaste"
            fin = FUENTE.render(f"Fin del juego: {resultado_final}", True, ROJO)
            VENTANA.blit(fin, (ANCHO // 2 - 150, ALTO // 2))
            pygame.display.flip()
            pygame.time.delay(4000)
            break

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
