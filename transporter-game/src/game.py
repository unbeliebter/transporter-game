import math

import pygame
import sys

from src.entity import Entity
from src.gamestats import Gamestats

# Initialisierung von Pygame
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption("Transporterspiel")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Schriftarten
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Entities
truck = Entity(75, 100, 500, 500, "resources/truck.png")
gas_station = Entity(200, 200, 750, 500, "resources/gas_station.png")
mineral = Entity(50, 50, 150, 150, "resources/mineral.png")
mine = Entity(200, 200, 100, 100, "resources/mine.png",)
fabric = Entity(200, 200, 900, 200, "resources/fabric.png")
helicopter = Entity(100, 100, 700, 200, "resources/helicopter.png")

entity_settings = {
    "capacity": "100",
    "consumption_truck": "10",
    "mineral_amount": "10",
    "speed_truck": "5.0",
    "speed_helicopter": "3.0",
    "win_percentage": "80",
}


# Schaltflächen-Funktion
def draw_button(screen, text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)


# Schieberegler-Funktion
def draw_text_input(screen, text, x, y, width, height, color, text_color, active):
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    text_surface = small_font.render(text, True, text_color)
    screen.blit(text_surface, (x + 5, y + 5))
    return pygame.Rect(x, y, width, height)


# Startbildschirm-Funktion
def start_screen(entity_settings):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game_loop(entity_settings)  # Wechsel zum Spiel
                elif settings_button.collidepoint(event.pos):
                    settings_screen(entity_settings)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(WHITE)

        # Schaltflächen
        start_button = draw_button(screen, "Start", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, GRAY, BLACK)
        settings_button = draw_button(screen, "Einstellungen", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, GRAY, BLACK)
        quit_button = draw_button(screen, "Schließen", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, BLACK)

        pygame.display.flip()


# Spiel-Funktion (einfaches Beispiel)
def game_loop(entity_settings):
    game_stats = Gamestats(truck, helicopter, entity_settings)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill("white")
        gas_station.draw(screen)
        mine.draw(screen)
        mineral.draw(screen)
        fabric.draw(screen)
        helicopter.draw(screen)

        keys = pygame.key.get_pressed()
        if any(keys):
            if keys[pygame.K_w]:
                truck.pos.y -= 300 * dt
                rotated_truck, rotated_rect = rotate_image(truck, 180)
                screen.blit(rotated_truck, rotated_rect)
            if keys[pygame.K_s]:
                truck.pos.y += 300 * dt
                rotated_truck, rotated_rect = rotate_image(truck, 0)
                screen.blit(rotated_truck, rotated_rect)
            if keys[pygame.K_a]:
                truck.pos.x -= 300 * dt
                rotated_truck, rotated_rect = rotate_image(truck, 270)
                screen.blit(rotated_truck, rotated_rect)
            if keys[pygame.K_d]:
                truck.pos.x += 300 * dt
                rotated_truck, rotated_rect = rotate_image(truck, 90)
                screen.blit(rotated_truck, rotated_rect)
        else:
            truck.draw(screen)

        track_truck(helicopter.pos, truck.pos, entity_settings["speed_helicopter"])

        # Kollision prüfen // muss
        check_collision(helicopter.pos, truck.pos)

    # flip() the display to put your work on screen
        pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
        dt = clock.tick(60) / 1000

def rotate_image(enity, angle):
    rotated_image = pygame.transform.rotate(enity.image, angle)
    rotated_rect = rotated_image.get_rect(center=enity.pos.center)

    return rotated_image, rotated_rect

def track_truck(helicopter_rect, truck_rect, speed):
    dx = truck_rect.centerx - helicopter_rect.centerx
    dy = truck_rect.centery - helicopter_rect.centery
    distance = math.sqrt(dx**2 + dy**2)
    if distance != 0:
        direction_x = dx / distance
        direction_y = dy / distance
        helicopter_rect.x += direction_x * float(speed)
        helicopter_rect.y += direction_y * float(speed)

def check_collision(helicopter_rect, item_rect):
    if helicopter_rect.colliderect(item_rect):
        return True
    return False

# Einstellungen-Funktion(einfaches Beispiel)
def settings_screen(entity_settings):
    text_inputs = {}
    active_input = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_input = None
                if save_button.collidepoint(event.pos):
                    game_loop(entity_settings)
                elif back_button.collidepoint(event.pos):
                    start_screen(entity_settings)
                for setting, rect in text_inputs.items():
                    if rect.collidepoint(event.pos):
                        active_input = setting
            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    active_input = None
                elif event.key == pygame.K_BACKSPACE:
                    entity_settings[active_input] = entity_settings[active_input][:-1]
                else:
                    entity_settings[active_input] += event.unicode

        screen.fill(WHITE)
        y_offset = 50
        for setting, value in entity_settings.items():
            text_surface = small_font.render(f"{setting}:", True, BLACK)
            screen.blit(text_surface, (50, y_offset))
            text_inputs[setting] = draw_text_input(
                screen, value, 300, y_offset, 100, 30, GRAY, BLACK, active_input == setting
            )
            y_offset += 50

            save_button = draw_button(screen, "Speichern und Spiel starten", 200, 600, 400, 50, GRAY, BLACK)
            back_button = draw_button(screen, "Speichern und Zurück", 700, 600, 300, 50, GRAY, BLACK)

        pygame.display.flip()


# Starten des Startbildschirms
start_screen(entity_settings)
