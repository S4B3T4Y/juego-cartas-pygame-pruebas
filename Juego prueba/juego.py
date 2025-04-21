import pygame
from cartas import generar_carta_aleatoria

# Colores
WHITE = (255, 255, 255)
GTRAY = (200, 200, 200)
GREEN = (0, 150, 0)
BLACK = (0, 0, 0)

class Carta:
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor