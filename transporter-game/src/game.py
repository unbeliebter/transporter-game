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

# Setzen des Rechtecks für die Spielinformationen im Fenster unten links
stats_rect = pygame.Rect(10, base.HEIGHT - 200, 250, 190)

# Das Spiel und dessen Logik
def game_loop(entity_settings):
    Gamestats(truck, helicopter, entity_settings)
    action_after_game = "menu"
    run = True

    # Das Spiel läuft in einer Schleife
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        base.screen.fill("white")

        # Alle Entities werden hier "gezeichnet"
        gas_station.draw(base.screen)
        mine.draw(base.screen)
        mineral.draw(base.screen)
        fabric.draw(base.screen)
        helicopter.draw(base.screen)

        # Hier ist die Bewegungslogik des LKWs
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        if any(keys):
            if keys[pygame.K_w]:
                truck.pos.y -= 300 * delta_time
                move_y -= 1
                rotated_truck, rotated_rect = helper.rotate_image(truck, 180)
                base.screen.blit(rotated_truck, rotated_rect)
            if keys[pygame.K_s]:
                truck.pos.y += 300 * delta_time
                move_y += 1
                rotated_truck, rotated_rect = helper.rotate_image(truck, 0)
                base.screen.blit(rotated_truck, rotated_rect)
            if keys[pygame.K_a]:
                truck.pos.x -= 300 * delta_time
                move_x -= 1
                rotated_truck, rotated_rect = helper.rotate_image(truck, 270)
                base.screen.blit(rotated_truck, rotated_rect)
            if keys[pygame.K_d]:
                truck.pos.x += 300 * delta_time
                move_x += 1
                rotated_truck, rotated_rect = helper.rotate_image(truck, 90)
                base.screen.blit(rotated_truck, rotated_rect)
        else:
            truck.draw(base.screen)

        # Hier wird für die Statistik der LKW-Richtung das Movement in ein Sting wie "Osten" umgewandelt
        if move_x != 0 or move_y != 0:
            angle_rad = math.atan2(move_y, move_x)
            angle_deg = math.degrees(angle_rad)
            truck.heading = get_direction_string(angle_deg)
        else:
            truck.heading = "Stehend"

        # Kommt der an der Mine an, so erhält der LKW das Mineral und in den Statistiken verliert die Mine ein Mineral
        if truck.pos.colliderect(mine.pos):
            if not truck.has_mineral:
                mine.act_items -= 1
                truck.has_mineral = True

        # Kommt der LKW an der Fabrik an, so wird das Mineral nicht mehr auf dem LKW angezeigt und die Fabrik erhält ein Mineral
        if truck.pos.colliderect(fabric.pos):
            if truck.has_mineral:
                fabric.act_items += 1
                truck.has_mineral = False

        # Funktion, dass der Helikopter den LKW verfolgt
        track_truck(helicopter.pos, truck.pos, entity_settings["speed_helicopter"])

        # Kommt der Helikopter in die Hitbox des LKWs so wird hier umgesetzt, dass dieser dem LKW das Mineral klaut.
        # Wenn das erfolgreich ist, so wird der Helikopter in die Startpostion gesetzt
        if helicopter.pos.colliderect(truck.pos):
            if truck.has_mineral:
                truck.has_mineral = False
                helicopter.has_mineral = True
                helicopter.pos.x = 700
                helicopter.pos.y = 200

        # Wenn der LKW ein Mineral bei der Fabrik geholt hat, wird das Mineral hier auf den LKW gezeichnet
        if truck.has_mineral:
            mineral_truck = BaseEntity(50, 50, truck.pos.x + 40, truck.pos.y + 40, "resources/mineral.png")
            mineral_truck.draw(base.screen)

        # Kommt der LKW an der Tankstelle vorbei, wird sein Tank auf 100% gesetzt
        if truck.pos.colliderect(gas_station.pos):
            truck.act_tank = 100

        # Hier wird geregelt, dass man mit dem LKW nicht außerhalb des Fensters fahren kann
        if truck.pos.left < 0:
            truck.pos.left = 0
        if truck.pos.right > base.WIDTH:
            truck.pos.right = base.WIDTH
        if truck.pos.top < 0:
            truck.pos.top = 0
        if truck.pos.bottom > base.HEIGHT:
            truck.pos.bottom = base.HEIGHT

        # Hier verliert der LKW den Tank im Zusammenhang mit dessen Verbrauch. Dieser kann auch nicht unter null fallen
        truck.act_tank -= truck.tank_loss
        if truck.act_tank < 0:
            truck.act_tank = 0

        # Zeichnen des Rechtecks für die Spielinformationen im Fenster unten links
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

        # Anzeigen aller gezeichneter Sachen auf dem Bildschirm
        pygame.display.flip()

        # Spielende-Bedingungen
        # Wenn der Tank leer ist, so verliert man das Spiel
        if truck.act_tank == 0:
            action_after_game = show_game_over(True, "Der Tank ist leer gegangen.")
            run = False

        # Wenn die Mineralien der Fabrik alle übergeben wurden, so gewinnt man das Spiel
        elif fabric.act_items == fabric.max_items:
            action_after_game = show_game_over(False,
                                               "Das Ziel der Mindestmineralien  wurde erreicht.")
            run = False

        #Wenn in der mine keine Mineralien mehr da sind und die Anzahl in der Fabrik nicht erreicht hat, so verliert man das Spiel
        elif mine.act_items == 0 and fabric.act_items != fabric.max_items:
            action_after_game = show_game_over(True, "Du hattest nicht genug Mineralien, um das Ziel zu erreichen.")
            run = False

        # Limitiert das Spiel auf 60 Frames per Second
        delta_time = clock.tick(60) / 1000

    return action_after_game

# Methode, dass der Helikopter den LKW verfolgt
def track_truck(helicopter_rect, truck_rect, speed):
    distance_x = truck_rect.centerx - helicopter_rect.centerx
    distance_y = truck_rect.centery - helicopter_rect.centery
    distance = math.sqrt(distance_x**2 + distance_y**2)
    if distance != 0:
        direction_x = distance_x / distance
        direction_y = distance_y / distance
        # Bewegung des Helikopters
        helicopter_rect.x += direction_x * float(speed)
        helicopter_rect.y += direction_y * float(speed)

# Bildschirm beim Gewinnen/Verlieren des Spiels mit benutzerdefiniertem Text
def show_game_over(game_over_flag, text):
    running_game_over_screen = True

    while running_game_over_screen:
        base.screen.fill("white")
        # Hier wird der Text gesetzt, ob man gewonnen/verloren hat inklusive Begründung
        if game_over_flag:
             text_surface = base.font.render("Du hast verloren! " + text, True, base.BLACK)
        else:
             text_surface = base.font.render("Du hast gewonnen! " + text, True, base.BLACK)
        text_rect = text_surface.get_rect(center=(base.WIDTH // 2, base.HEIGHT // 4))
        base.screen.blit(text_surface, text_rect)

        # Zeichnen der Buttons für den Game-Over-Bildschirm
        button_replay_rect = helper.draw_button(base.screen, "Nochmal spielen", base.WIDTH // 2 - 100, base.HEIGHT // 2 - 100, 200, 50, base.GRAY, base.BLACK)
        button_menu_rect = helper.draw_button(base.screen, "Zum Hauptmenü", base.WIDTH // 2 - 100, base.HEIGHT // 2, 200, 50, base.GRAY, base.BLACK)
        button_close_rect = helper.draw_button(base.screen, "Schließen", base.WIDTH // 2 - 100, base.HEIGHT // 2 + 100, 200, 50, base.GRAY, base.BLACK)

        # Event-Handling für Klicken
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            #Hier sind die jeweiligen Bildschirme definiert, die dann bei Klick zurückgegeben werden
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_close_rect.collidepoint(event.pos):
                    running_game_over_screen = False
                    return "quit"
                elif button_replay_rect.collidepoint(event.pos):
                    running_game_over_screen = False
                    return "replay"
                elif button_menu_rect.collidepoint(event.pos):
                    running_game_over_screen = False
                    return "menu"

        pygame.display.flip()

# Bildschirm der Einstellungen
def settings_screen(entity_settings):
    text_inputs = {}
    active_input = None
    # Kopieren der Einstellungen zum Editieren
    local_settings = entity_settings.copy()

    while True:
        base.screen.fill(base.WHITE)
        y_offset = 50
        for setting, value in local_settings.items():
            # Erstellen der Texte für die Einstellungen
            text_surface = base.small_font.render(f"{setting}:", True, base.BLACK)
            base.screen.blit(text_surface, (50, y_offset))
            text_inputs[setting] = helper.draw_text_input(
                base.screen, value, 300, y_offset, 100, 30, base.GRAY, base.BLACK, active_input == setting
            )
            y_offset += 50

        # Buttons zeichnen zum Speichern/Spielen
        save_button_rect = helper.draw_button(base.screen, "Speichern und Spiel starten", 200, 600, 400, 50, base.GRAY, base.BLACK)
        back_button_rect = helper.draw_button(base.screen, "Speichern und Zurück", 700, 600, 300, 50, base.GRAY, base.BLACK)


        # Event-Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_input = None

                # Hier sind die jeweiligen Bildschirme definiert, die dann bei Klick zurückgegeben werden
                if save_button_rect.collidepoint(event.pos):
                    entity_settings.update(local_settings)
                    return "start_game"
                elif back_button_rect.collidepoint(event.pos):
                    entity_settings.update(local_settings)
                    return "menu"


                for setting, rect in text_inputs.items():
                    if rect.collidepoint(event.pos):
                        active_input = setting

            # Felder-Aktionen Eingabe der Einstellungen
            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    active_input = None
                elif event.key == pygame.K_BACKSPACE:
                    local_settings[active_input] = local_settings[active_input][:-1]
                else:
                    local_settings[active_input] += event.unicode

        pygame.display.flip()


# Der Startbildschirm und dessen Buttons
def start_screen(entity_settings):
    while True:
        base.screen.fill("white")

        # Buttons des Start-Bildschirms
        start_button_rect = helper.draw_button(base.screen, "Start", base.WIDTH // 2 - 100, base.HEIGHT // 2 - 100, 200, 50, base.GRAY, base.BLACK)
        settings_button_rect = helper.draw_button(base.screen, "Einstellungen", base.WIDTH // 2 - 100, base.HEIGHT // 2, 200, 50, base.GRAY, base.BLACK)
        quit_button_rect = helper.draw_button(base.screen, "Schließen", base.WIDTH // 2 - 100, base.HEIGHT // 2 + 100, 200, 50, base.GRAY, base.BLACK)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            # Hier sind die jeweiligen Bildschirme definiert, die dann bei Klick zurückgegeben werden
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "start_game"
                elif settings_button_rect.collidepoint(event.pos):
                    return "settings"
                elif quit_button_rect.collidepoint(event.pos):
                    return "quit"

        pygame.display.flip()

# Beim erneuten Spielen werden alle Werte auf die Anfangswerte gesetzt
def reset_game_state(settings):
    global truck, mine, fabric, helicopter

    # LKW
    truck.pos.x, truck.pos.y = 500, 500
    truck.act_tank = 100
    truck.has_mineral = False
    truck.tank_loss = float(settings["consumption_truck"]) / 100 #

    # Mine
    mine.max_items = int(settings["mineral_amount"])
    mine.act_items = int(settings["mineral_amount"])

    # Fabrik
    fabric.max_items = int(int(settings["mineral_amount"]) * (float(settings["win_percentage"])) / 100)
    fabric.act_items = 0

    # Helikopter
    helicopter.pos.x, helicopter.pos.y = 700, 200
    helicopter.has_mineral = False

# Verwaltung der Spiel-Bildschirme
def main():
    current_screen = "menu"
    game_settings = entity_settings.copy()

    # Auswahl der Bildschirme
    while current_screen != "quit":
        if current_screen == "menu":
            current_screen = start_screen(game_settings)
        elif current_screen == "settings":
            current_screen = settings_screen(game_settings)
        elif current_screen == "start_game":
            #Beim Start des Spiels wird immer alles auf die Standardwerte zurückgesetzt
            reset_game_state(game_settings)
            current_screen = "game"
        elif current_screen == "game":
            action_after_game = game_loop(game_settings)
            if action_after_game == "replay":
                current_screen = "start_game"
            elif action_after_game == "menu":
                current_screen = "menu"
            elif action_after_game == "quit":
                current_screen = "quit"

    pygame.quit()
    sys.exit()

# Starten der Hauptfunktion
if __name__ == "__main__":
    main()
