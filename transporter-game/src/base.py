import pygame, pathlib

# Diese Klasse besitzt Standarddaten, die von mehreren Klassen genutzt werden, wie bspw. Schriftarten

# Bildschirmauflösung
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Schriftarten
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
xtra_small_font = pygame.font.Font(None, 17)