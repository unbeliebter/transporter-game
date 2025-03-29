from pygame import Rect

from src.entity import Entity


class Counter(Entity):
    max_items = 0
    act_items = 0

    def __init__(self, max_items, act_items, width, height, pos_x, pos_y, image_path):
        super().__init__(width, height, pos_x, pos_y, image_path)
        self.max_items = max_items
        self.act_items = act_items