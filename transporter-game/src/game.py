import math

import pygame
import sys

from src import helper, base
from src.counter import Counter
from src.baseEntity import BaseEntity
from src.gamestats import Gamestats
from src.vehicle import Vehicle
from src.helper import get_direction_string

# Initialisierung von Pygame und Basisvariablen
pygame.init()
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption("Transporterspiel")

#Die möglichen Einstellungen des Spiels als Dictionary
entity_settings = {
    "capacity": "100",
    "consumption_truck": "10.0",
    "mineral_amount": "10",
    "speed_truck": "5.0",
    "speed_helicopter": "2.0",
    "win_percentage": "80",
}

# Alle Entity-Definitionen
truck = Vehicle(100, entity_settings["capacity"], False, float(entity_settings["consumption_truck"]) / 100,  75, 100, 500, 500, "resources/truck.png")
gas_station = BaseEntity(200, 200, 750, 500, "resources/gas_station.png")
mineral = BaseEntity(50, 50, 150, 150, "resources/mineral.png")
mine = Counter(int(entity_settings["mineral_amount"]), int(entity_settings["mineral_amount"]), 200, 200, 100, 100, "resources/mine.png",)
fabric = Counter(int(int(entity_settings["mineral_amount"]) * (float(entity_settings["win_percentage"])) / 100), 0, 200, 200, 900, 200, "resources/fabric.png")
helicopter = Vehicle(0, 0, False, 0, 100, 100, 700, 200, "resources/helicopter.png")

stats_rect = pygame.Rect(10, base.HEIGHT - 200, 250, 190)

# Das Spiel und dessen Logik
def game_loop(entity_settings):
    game_stats = Gamestats(truck, helicopter, entity_settings)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        base.screen.fill("white")
        gas_station.draw(base.screen)
        mine.draw(base.screen)
        mineral.draw(base.screen)
        fabric.draw(base.screen)
        helicopter.draw(base.screen)

        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        if any(keys):
            if keys[pygame.K_w]:
                truck.pos.y -= 300 * dt
                move_y -= 1
                rotated_truck, rotated_rect = helper.rotate_image(truck, 180)
                base.screen.blit(rotated_truck, rotated_rect)
            if keys[pygame.K_s]:
                truck.pos.y += 300 * dt
                move_y += 1
                rotated_truck, rotated_rect = helper.rotate_image(truck, 0)
                base.screen.blit(rotated_truck, rotated_rect)
            if keys[pygame.K_a]:
                truck.pos.x -= 300 * dt
                move_x -= 1
                rotated_truck, rotated_rect = helper.rotate_image(truck, 270)
                base.screen.blit(rotated_truck, rotated_rect)
            if keys[pygame.K_d]:
                truck.pos.x += 300 * dt
                move_x += 1
                rotated_truck, rotated_rect = helper.rotate_image(truck, 90)
                base.screen.blit(rotated_truck, rotated_rect)
        else:
            truck.draw(base.screen)

        if move_x != 0 or move_y != 0:
            angle_rad = math.atan2(move_y, move_x)
            angle_deg = math.degrees(angle_rad)
            truck.heading = get_direction_string(angle_deg)
        else:
            truck.heading = "Stehend"

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
                helicopter.pos.x = 700
                helicopter.pos.y = 200

        if truck.has_mineral:
            mineral_truck = BaseEntity(50, 50, truck.pos.x + 40, truck.pos.y + 40, "resources/mineral.png")
            mineral_truck.draw(base.screen)

#        elif helicopter.has_mineral:
#            mineral_heli = Entity(50, 50, helicopter.pos.x + 40, helicopter.pos.y + 40, "resources/mineral.png")
#            mineral_heli.draw(screen)

        if truck.pos.colliderect(gas_station.pos):
            truck.act_tank = 100

        if truck.pos.left < 0:
            truck.pos.left = 0
        if truck.pos.right > base.WIDTH:
            truck.pos.right = base.WIDTH
        if truck.pos.top < 0:
            truck.pos.top = 0
        if truck.pos.bottom > base.HEIGHT:
            truck.pos.bottom = base.HEIGHT

        truck.act_tank -= truck.tank_loss
        if truck.act_tank < 0:
            truck.act_tank = 0

        if truck.act_tank == 0:
            game_stats.game_over = True
            show_game_over(game_stats.game_over, "Der Tank ist leer gegangen")
            run = False

        pygame.draw.rect(base.screen, base.GRAY, stats_rect, 2)

        # Spielstatistiken rendern
        text_pos_helicopter = base.xtra_small_font.render(f"Heli-Pos: {helicopter.pos}", True, base.BLACK)
        text_pos_truck = base.xtra_small_font.render(f"LKW-Pos: {truck.pos}", True, base.BLACK)
        text_speed_helicopter = base.xtra_small_font.render(f"Heli-Geschw.: {entity_settings["speed_helicopter"]}", True, base.BLACK)
        text_speed_truck = base.xtra_small_font.render(f"LKW-Geschw.: {entity_settings["speed_truck"]}", True, base.BLACK)
        text_direction_truck = base.xtra_small_font.render(f"LKW-Richtung: {truck.heading}", True, base.BLACK)
        text_truck_tank = base.xtra_small_font.render(f"LKW-Tank: {int(((truck.act_tank / int(truck.max_tank)) * 100))}%", True, base.BLACK)
        text_mineral_truck = base.xtra_small_font.render(f"LKW-Mineral: {truck.has_mineral}", True, base.BLACK)
        text_mineral_mine = base.xtra_small_font.render(f"Mine-Mineral: {mine.act_items} / {mine.max_items}", True,
                                        base.BLACK)
        text_mineral_fabric = base.xtra_small_font.render(
            f"Fabrik-Mineral: {fabric.act_items} / {fabric.max_items}", True, base.BLACK)

        # Spielstatistiken auf dem Bildschirm anzeigen
        base.screen.blit(text_pos_helicopter, (stats_rect.x + 10, stats_rect.y + 10))
        base.screen.blit(text_pos_truck, (stats_rect.x + 10, stats_rect.y + 30))
        base.screen.blit(text_speed_helicopter, (stats_rect.x + 10, stats_rect.y + 50))
        base.screen.blit(text_speed_truck, (stats_rect.x + 10, stats_rect.y + 70))
        base.screen.blit(text_direction_truck, (stats_rect.x + 10, stats_rect.y + 90))
        base.screen.blit(text_truck_tank, (stats_rect.x + 10, stats_rect.y + 110))
        base.screen.blit(text_mineral_truck, (stats_rect.x + 10, stats_rect.y + 130))
        base.screen.blit(text_mineral_mine, (stats_rect.x + 10, stats_rect.y + 150))
        base.screen.blit(text_mineral_fabric, (stats_rect.x + 10, stats_rect.y + 170))

    # flip() the display to put your work on screen
        pygame.display.flip()

        if fabric.act_items == fabric.max_items:
            show_game_over(game_stats.game_over, "Das Ziel der mindest Mineralien wurde erreicht")
            run = False

        if mine.act_items == 0 and fabric.act_items != fabric.max_items:
            game_stats.game_over = True
            show_game_over(game_stats.game_over, "Du hast nicht genug Mineralien, um das Ziel zu erreichen")
            run = False

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
        dt = clock.tick(60) / 1000

def track_truck(helicopter_rect, truck_rect, speed):
    dx = truck_rect.centerx - helicopter_rect.centerx
    dy = truck_rect.centery - helicopter_rect.centery
    distance = math.sqrt(dx**2 + dy**2)
    if distance != 0:
        direction_x = dx / distance
        direction_y = dy / distance
        helicopter_rect.x += direction_x * float(speed)
        helicopter_rect.y += direction_y * float(speed)

def show_game_over(game_over, label):

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
            text_surface = base.font.render("Du hast verloren! " + label, True, base.BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = (base.WIDTH // 2, base.HEIGHT // 4)
            base.screen.fill("white")
            base.screen.blit(text_surface, text_rect)
        else:
            text_surface = base.font.render("Du hast gewonnen! " + label, True, base.BLACK)
            text_rect = text_surface.get_rect()
            text_rect.center = (base.WIDTH // 2, base.HEIGHT // 4)
            base.screen.fill("white")
            base.screen.blit(text_surface, text_rect)

        button_replay = helper.draw_button(base.screen, "Nochmal spielen", base.WIDTH // 2 - 100, base.HEIGHT // 2 - 100, 200, 50, base.GRAY, base.BLACK)
        button_menu = helper.draw_button(base.screen, "Zum Hauptmenü", base.WIDTH // 2 - 100, base.HEIGHT // 2, 200, 50, base.GRAY, base.BLACK)
        button_close = helper.draw_button(base.screen, "Schließen", base.WIDTH // 2 - 100, base.HEIGHT // 2 + 100, 200, 50, base.GRAY, base.BLACK)

        pygame.display.flip()

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

        base.screen.fill(base.WHITE)
        y_offset = 50
        for setting, value in entity_settings.items():
            text_surface = base.small_font.render(f"{setting}:", True, base.BLACK)
            base.screen.blit(text_surface, (50, y_offset))
            text_inputs[setting] = helper.draw_text_input(
                base.screen, value, 300, y_offset, 100, 30, base.GRAY, base.BLACK, active_input == setting
            )
            y_offset += 50

            save_button = helper.draw_button(base.screen, "Speichern und Spiel starten", 200, 600, 400, 50, base.GRAY, base.BLACK)
            back_button = helper.draw_button(base.screen, "Speichern und Zurück", 700, 600, 300, 50, base.GRAY, base.BLACK)

        pygame.display.flip()

# Der Startbildschirm und dessen Buttons
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

        base.screen.fill("white")

        # Definitionen der Buttons des Startbildschirms
        start_button = helper.draw_button(base.screen, "Start", base.WIDTH // 2 - 100, base.HEIGHT // 2 - 100, 200, 50, base.GRAY, base.BLACK)
        settings_button = helper.draw_button(base.screen, "Einstellungen", base.WIDTH // 2 - 100, base.HEIGHT // 2, 200, 50, base.GRAY, base.BLACK)
        quit_button = helper.draw_button(base.screen, "Schließen", base.WIDTH // 2 - 100, base.HEIGHT // 2 + 100, 200, 50, base.GRAY, base.BLACK)

        pygame.display.flip()

# Starten des Startbildschirms
start_screen(entity_settings)
