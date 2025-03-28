import pygame
from pygame import Surface, Rect, transform


class Entity:
    __image = Surface
    pos = Rect

    __width = 0
    __height = 0

    def draw(self, screen):
        screen.blit(self.__image, self.pos)

    def __init__(self, width, height, pos_x, pos_y, image_path):
        image = pygame.image.load(image_path)

        self.__image = transform.scale(image, (width, height))
        self.__width = width
        self.__height = height
        self.pos = self.__image.get_rect(center=(pos_x, pos_y))

