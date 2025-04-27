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
    action_after_game = "menu"
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

        if truck.act_tank == 0:
            action_after_game = show_game_over(True, "Der Tank ist leer gegangen")
            run = False  # Beende die game_loop
        elif fabric.act_items == fabric.max_items:  # Use elif to avoid multiple game_over calls
            action_after_game = show_game_over(False,
                                               "Das Ziel der mindest Mineralien wurde erreicht")  # game_over=False for win
            run = False  # Beende die game_loop
        elif mine.act_items == 0 and fabric.act_items != fabric.max_items:
            action_after_game = show_game_over(True, "Du hast nicht genug Mineralien, um das Ziel zu erreichen")
            run = False  # Beende die game_loop

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
        dt = clock.tick(60) / 1000
    return action_after_game

def track_truck(helicopter_rect, truck_rect, speed):
    dx = truck_rect.centerx - helicopter_rect.centerx
    dy = truck_rect.centery - helicopter_rect.centery
    distance = math.sqrt(dx**2 + dy**2)
    if distance != 0:
        direction_x = dx / distance
        direction_y = dy / distance
        helicopter_rect.x += direction_x * float(speed)
        helicopter_rect.y += direction_y * float(speed)

def show_game_over(game_over_flag, label):
    running_game_over_screen = True
    while running_game_over_screen:
        # --- 1. Zeichnen des Hintergrunds und Textes ---
        base.screen.fill("white")
        if game_over_flag:
             text_surface = base.font.render("Du hast verloren! " + label, True, base.BLACK)
        else:
             text_surface = base.font.render("Du hast gewonnen! " + label, True, base.BLACK)
        text_rect = text_surface.get_rect(center=(base.WIDTH // 2, base.HEIGHT // 4))
        base.screen.blit(text_surface, text_rect)

        # --- 2. Buttons zeichnen UND deren Rects für DIESEN Frame speichern ---
        button_replay_rect = helper.draw_button(base.screen, "Nochmal spielen", base.WIDTH // 2 - 100, base.HEIGHT // 2 - 100, 200, 50, base.GRAY, base.BLACK)
        button_menu_rect = helper.draw_button(base.screen, "Zum Hauptmenü", base.WIDTH // 2 - 100, base.HEIGHT // 2, 200, 50, base.GRAY, base.BLACK)
        button_close_rect = helper.draw_button(base.screen, "Schließen", base.WIDTH // 2 - 100, base.HEIGHT // 2 + 100, 200, 50, base.GRAY, base.BLACK)

        # --- 3. Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                # --- 4. Kollision mit den GESPEICHERTEN Rects prüfen ---
                if button_close_rect.collidepoint(event.pos):
                    running_game_over_screen = False
                    return "quit" # Signal to quit
                elif button_replay_rect.collidepoint(event.pos):
                    running_game_over_screen = False
                    return "replay" # Signal to replay
                elif button_menu_rect.collidepoint(event.pos):
                    running_game_over_screen = False
                    return "menu" # Signal to go to menu

        # --- 5. Display aktualisieren ---
        pygame.display.flip()

# Einstellungen-Funktion(einfaches Beispiel)
def settings_screen(entity_settings):
    text_inputs = {}
    active_input = None
    # Need local copy of settings to allow changes without affecting current game until saved
    local_settings = entity_settings.copy()

    while True:
        # --- Zeichnen des Einstellungsbildschirms (Buttons und Inputs hier zeichnen!) ---
        base.screen.fill(base.WHITE)
        y_offset = 50
        # Use local_settings for displaying and editing
        for setting, value in local_settings.items():
            text_surface = base.small_font.render(f"{setting}:", True, base.BLACK)
            base.screen.blit(text_surface, (50, y_offset))
            # Draw text input and get its Rect
            text_inputs[setting] = helper.draw_text_input(
                base.screen, value, 300, y_offset, 100, 30, base.GRAY, base.BLACK, active_input == setting
            )
            y_offset += 50

        # Buttons zeichnen UND deren Rects für DIESEN Frame speichern
        save_button_rect = helper.draw_button(base.screen, "Speichern und Spiel starten", 200, 600, 400, 50, base.GRAY, base.BLACK)
        back_button_rect = helper.draw_button(base.screen, "Speichern und Zurück", 700, 600, 300, 50, base.GRAY, base.BLACK)


        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit" # Signal to quit from settings
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_input = None # Deactivate current input on any mouse click not on an input box

                # Kollision mit den GESPEICHERTEN Button Rects prüfen
                if save_button_rect.collidepoint(event.pos):
                    # Apply settings back to the main settings dict (or return them)
                    entity_settings.update(local_settings) # Update the main settings
                    print("Einstellungen gespeichert. Starte Spiel...")
                    return "start_game" # Signal to start game with new settings
                elif back_button_rect.collidepoint(event.pos):
                    # Apply settings
                    entity_settings.update(local_settings) # Update the main settings
                    print("Einstellungen gespeichert. Zurück zum Menü...")
                    return "menu" # Signal to go back to menu

                # Check collision for text inputs *after* checking buttons
                # This part is already done correctly in your original code's logic flow
                for setting, rect in text_inputs.items():
                    if rect.collidepoint(event.pos):
                        active_input = setting
                        print(f"Active input: {active_input}") # Debug print

            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    active_input = None
                elif event.key == pygame.K_BACKSPACE:
                    local_settings[active_input] = local_settings[active_input][:-1]
                else:
                    # Only allow numeric input for specific settings if needed
                    # if active_input in ["capacity", "mineral_amount", "win_percentage"]:
                    #     if event.unicode.isdigit():
                    #         local_settings[active_input] += event.unicode
                    # elif active_input in ["consumption_truck", "speed_truck", "speed_helicopter"]:
                    #      if event.unicode.isdigit() or event.unicode == '.':
                    #          local_settings[active_input] += event.unicode
                    # else: # Allow any character for other settings (if any)
                    #     local_settings[active_input] += event.unicode
                    local_settings[active_input] += event.unicode # Keeping original simple keydown handling


        # --- Display aktualisieren ---
        pygame.display.flip()


# Der Startbildschirm und dessen Buttons
def start_screen(entity_settings):
    while True:
        # --- Zeichnen des Startbildschirms (Buttons hier zeichnen!) ---
        base.screen.fill("white")

        # Buttons zeichnen UND deren Rects für DIESEN Frame speichern
        start_button_rect = helper.draw_button(base.screen, "Start", base.WIDTH // 2 - 100, base.HEIGHT // 2 - 100, 200, 50, base.GRAY, base.BLACK)
        settings_button_rect = helper.draw_button(base.screen, "Einstellungen", base.WIDTH // 2 - 100, base.HEIGHT // 2, 200, 50, base.GRAY, base.BLACK)
        quit_button_rect = helper.draw_button(base.screen, "Schließen", base.WIDTH // 2 - 100, base.HEIGHT // 2 + 100, 200, 50, base.GRAY, base.BLACK)

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit" # Signal to quit from start screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kollision mit den GESPEICHERTEN Rects prüfen
                if start_button_rect.collidepoint(event.pos):
                    print("Starte Spiel...") # Debug print
                    return "start_game" # Signal to start game
                elif settings_button_rect.collidepoint(event.pos):
                    print("Gehe zu Einstellungen...") # Debug print
                    return "settings" # Signal to go to settings
                elif quit_button_rect.collidepoint(event.pos):
                    print("Schließe Spiel...") # Debug print
                    return "quit" # Signal to quit

        # --- Display aktualisieren ---
        pygame.display.flip()

def reset_game_state(settings):
    global truck, mine, fabric, helicopter # Muss globale Variablen deklarieren, wenn sie neu zugewiesen werden
    # Oder besser: Die __init__ Methoden auf den bestehenden Objekten aufrufen, falls das möglich ist
    # truck.__init__(100, settings["capacity"], False, float(settings["consumption_truck"]) / 100,  75, 100, 500, 500, "resources/truck.png")
    # mine.__init__(int(settings["mineral_amount"]), int(settings["mineral_amount"]), 200, 200, 100, 100, "resources/mine.png")
    # fabric.__init__(int(int(settings["mineral_amount"]) * (float(settings["win_percentage"])) / 100), 0, 200, 200, 900, 200, "resources/fabric.png")
    # helicopter.__init__(0, 0, False, 0, 100, 100, 700, 200, "resources/helicopter.png")
    # Wenn die Klassen __init__ keine Neupositionierung machen, musst du die pos-Attribute manuell zurücksetzen:
    truck.pos.x, truck.pos.y = 500, 500
    truck.act_tank = 100
    truck.has_mineral = False
    truck.tank_loss = float(settings["consumption_truck"]) / 100 # Aus Settings übernehmen

    mine.max_items = int(settings["mineral_amount"]) # Aus Settings übernehmen
    mine.act_items = int(settings["mineral_amount"]) # Auf Max zurücksetzen

    fabric.max_items = int(int(settings["mineral_amount"]) * (float(settings["win_percentage"])) / 100) # Aus Settings übernehmen
    fabric.act_items = 0 # Auf 0 zurücksetzen

    helicopter.pos.x, helicopter.pos.y = 700, 200 # Auf Startposition zurücksetzen
    helicopter.has_mineral = False # Helikopter hat kein Mineral am Start

    # gas_station und mineral müssen wahrscheinlich nicht zurückgesetzt werden, da sie sich nicht ändern

# Hauptfunktion zur Verwaltung der Spielzustände
def main():
    current_state = "menu" # Start with the menu
    game_settings = entity_settings.copy() # Use a copy of settings

    while current_state != "quit":
        if current_state == "menu":
            current_state = start_screen(game_settings) # start_screen returns next state
        elif current_state == "settings":
            current_state = settings_screen(game_settings) # settings_screen returns next state
        elif current_state == "start_game":
            # --- SPIELZUSTAND ZURÜCKSETZEN VOR DEM START ---
            reset_game_state(game_settings)
            current_state = "game" # Now enter the game loop
        elif current_state == "game":
            # game_loop returns the action requested after game end
            action_after_game = game_loop(game_settings)
            # Handle the action returned by game_loop
            if action_after_game == "replay":
                current_state = "start_game" # Go back to "start_game" state to trigger reset and restart
            elif action_after_game == "menu":
                current_state = "menu" # Go back to menu
            elif action_after_game == "quit":
                current_state = "quit" # Quit the main loop

    pygame.quit()
    sys.exit()

# Starten der Hauptfunktion
if __name__ == "__main__":
    main()
