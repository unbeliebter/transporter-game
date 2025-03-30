import math

import pygame
import sys

from src.counter import Counter
from src.entity import Entity
from src.gamestats import Gamestats
from src.vehicle import Vehicle

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
xtra_small_font = pygame.font.Font(None, 17)

entity_settings = {
    "capacity": "100",
    "consumption_truck": "10.0",
    "mineral_amount": "10",
    "speed_truck": "5.0",
    "speed_helicopter": "2.0",
    "win_percentage": "80",
}

# Entities
truck = Vehicle(100, entity_settings["capacity"], False, float(entity_settings["consumption_truck"]) / 100,  75, 100, 500, 500, "resources/truck.png")
gas_station = Entity(200, 200, 750, 500, "resources/gas_station.png")
mineral = Entity( 50, 50, 150, 150, "resources/mineral.png")
mine = Counter(int(entity_settings["mineral_amount"]), int(entity_settings["mineral_amount"]), 200, 200, 100, 100, "resources/mine.png",)
fabric = Counter(int(int(entity_settings["mineral_amount"]) * (float(entity_settings["win_percentage"])) / 100), 0, 200, 200, 900, 200, "resources/fabric.png")
helicopter = Vehicle(0, 0, False, 0, 100, 100, 700, 200, "resources/helicopter.png")


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

        background_image = pygame.image.load("resources/start_screen.png")
        scaled_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

        screen.blit(scaled_image, (0,0))

        # Schaltflächen
        start_button = draw_button(screen, "Start", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, GRAY, BLACK)
        settings_button = draw_button(screen, "Einstellungen", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, GRAY, BLACK)
        quit_button = draw_button(screen, "Schließen", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, BLACK)

        pygame.display.flip()

stats_rect = pygame.Rect(10, HEIGHT - 200, 250, 190)

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

        if truck.pos.colliderect(mine.pos):
            if not truck.has_mineral:
                mine.act_items -= 1
                truck.has_mineral = True

        if truck.pos.colliderect(fabric.pos):
            if truck.has_mineral:
                fabric.act_items += 1
                truck.has_mineral = False

        track_truck(helicopter.pos, truck.pos, entity_settings["speed_helicopter"])

        if helicopter.pos.colliderect(truck.pos):
            if truck.has_mineral:
                truck.has_mineral = False
                helicopter.has_mineral = True

        if truck.has_mineral:
            mineral_truck = Entity(50, 50, truck.pos.x + 40, truck.pos.y + 40, "resources/mineral.png")
            mineral_truck.draw(screen)
        elif helicopter.has_mineral:
            mineral_heli = Entity(50, 50, helicopter.pos.x + 40, helicopter.pos.y + 40, "resources/mineral.png")
            mineral_heli.draw(screen)

        if truck.pos.colliderect(gas_station.pos):
            truck.act_tank = 100

        if truck.pos.left < 0:
            truck.pos.left = 0
        if truck.pos.right > WIDTH:
            truck.pos.right = WIDTH
        if truck.pos.top < 0:
            truck.pos.top = 0
        if truck.pos.bottom > HEIGHT:
            truck.pos.bottom = HEIGHT

        truck.act_tank -= truck.tank_loss
        if truck.act_tank < 0:
            truck.act_tank = 0

        if truck.act_tank == 0:
            game_stats.game_over = True
            show_game_over(game_stats.game_over)

        pygame.draw.rect(screen, GRAY, stats_rect, 2)

        # Spielstatistiken rendern
        text_pos_helicopter = xtra_small_font.render(f"Heli-Pos: {helicopter.pos}", True, BLACK)
        text_pos_truck = xtra_small_font.render(f"LKW-Pos: {truck.pos}", True, BLACK)
        text_speed_helicopter = xtra_small_font.render(f"Heli-Geschw.: {entity_settings["speed_helicopter"]}", True, BLACK)
        text_speed_truck = xtra_small_font.render(f"LKW-Geschw.: {entity_settings["speed_truck"]}", True, BLACK)
        text_direction_truck = xtra_small_font.render(f"LKW-Richtung: {truck.heading}", True, BLACK)
        text_truck_tank = xtra_small_font.render(f"LKW-Tank: {int(((truck.act_tank / int(truck.max_tank)) * 100))}%", True, BLACK)
        text_mineral_truck = xtra_small_font.render(f"LKW-Mineral: {truck.has_mineral}", True, BLACK)
        text_mineral_mine = xtra_small_font.render(f"Mine-Mineral: {mine.act_items} / {mine.max_items}", True,
                                        BLACK)
        text_mineral_fabric = xtra_small_font.render(
            f"Fabrik-Mineral: {fabric.act_items} / {fabric.max_items}", True, BLACK)

        # Spielstatistiken auf dem Bildschirm anzeigen
        screen.blit(text_pos_helicopter, (stats_rect.x + 10, stats_rect.y + 10))
        screen.blit(text_pos_truck, (stats_rect.x + 10, stats_rect.y + 30))
        screen.blit(text_speed_helicopter, (stats_rect.x + 10, stats_rect.y + 50))
        screen.blit(text_speed_truck, (stats_rect.x + 10, stats_rect.y + 70))
        screen.blit(text_direction_truck, (stats_rect.x + 10, stats_rect.y + 90))
        screen.blit(text_truck_tank, (stats_rect.x + 10, stats_rect.y + 110))
        screen.blit(text_mineral_truck, (stats_rect.x + 10, stats_rect.y + 130))
        screen.blit(text_mineral_mine, (stats_rect.x + 10, stats_rect.y + 150))
        screen.blit(text_mineral_fabric, (stats_rect.x + 10, stats_rect.y + 170))

    # flip() the display to put your work on screen
        pygame.display.flip()

        if fabric.act_items == fabric.max_items:
            show_game_over(game_stats.game_over)

        if mine.act_items == 0 and fabric.act_items != fabric.max_items:
            game_stats.game_over = True
            show_game_over(game_stats.game_over)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
        dt = clock.tick(60) / 1000

def rotate_image(entity, angle):
    rotated_image = pygame.transform.rotate(entity.image, angle)
    rotated_rect = rotated_image.get_rect(center=entity.pos.center)

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

# Funktion zum Anzeigen des Gewinner-/Verliererfensters
def show_game_over(game_over):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_close.collidepoint(event.pos):
                    pygame.quit()
                    return
                elif button_replay.collidepoint(event.pos):
                    game_loop(entity_settings)
                elif button_menu.collidepoint(event.pos):
                    start_screen(entity_settings)

        if game_over:
            background_image = pygame.image.load("resources/game_over_lose.jpg")
            scaled_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            screen.blit(scaled_image, (0, 0))
        else:
            background_image = pygame.image.load("resources/game_over_win.jpg")
            scaled_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            screen.blit(scaled_image, (0, 0))

        button_replay = draw_button(screen, "Nochmal spielen", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, GRAY, BLACK)
        button_menu = draw_button(screen, "Zum Hauptmenü", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, GRAY, BLACK)
        button_close = draw_button(screen, "Schließen", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, GRAY, BLACK)

        pygame.display.flip()

# Starten des Startbildschirms
start_screen(entity_settings)
