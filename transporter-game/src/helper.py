import pygame

from src import base

def get_direction_string(angle_degrees):
    angle = (angle_degrees + 360) % 360

    if 337.5 <= angle or angle < 22.5:
        return "Osten"
    elif 22.5 <= angle < 67.5:
        return "Südosten"
    elif 67.5 <= angle < 112.5:
        return "Süden"
    elif 112.5 <= angle < 157.5:
        return "Südwesten"
    elif 157.5 <= angle < 202.5:
        return "Westen"
    elif 202.5 <= angle < 247.5:
        return "Nordwesten"
    elif 247.5 <= angle < 292.5:
        return "Norden"
    elif 292.5 <= angle < 337.5:
        return "Nordosten"
    else:
        return "Unbekannt" # Sollte bei normalen Winkeln nicht vorkommen

# Schaltflächen-Funktion
def draw_button(screen, text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = base.font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)

# Schieberegler-Funktion
def draw_text_input(screen, text, x, y, width, height, color, text_color, active):
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    text_surface = base.small_font.render(text, True, text_color)
    screen.blit(text_surface, (x + 5, y + 5))
    return pygame.Rect(x, y, width, height)

def rotate_image(entity, angle):
    rotated_image = pygame.transform.rotate(entity.image, angle)
    rotated_rect = rotated_image.get_rect(center=entity.pos.center)

    return rotated_image, rotated_rect