from pygame import Rect

from src.entity import Entity


class Vehicle(Entity):
    act_tank = 0
    max_tank = 100
    has_mineral = False
    heading = Rect

    def __init__(self, act_tank, max_tank, has_mineral, width, height, pos_x, pos_y, image_path):
        super().__init__(width, height, pos_x, pos_y, image_path)
        self.act_tank = act_tank
        self.max_tank = max_tank
        self.has_mineral = has_mineral
