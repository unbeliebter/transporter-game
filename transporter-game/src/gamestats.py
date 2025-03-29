from pygame import Rect


class Gamestats:
    pos_helicopter = Rect
    pos_truck = Rect

    speed_helicopter = 0
    speed_truck = 0
    direction_truck = Rect
    truck_tank = 0

    mineral_truck = False
    mineral_mine = 0
    mineral_mine_start = 0
    mineral_fabric = 0
    mineral_fabric_start = 0

    game_over = False

    def __init__(self, truck, helicopter, entity_settings):
        self.pos_helicopter = helicopter.pos
        self.pos_truck = truck.pos
        self.speed_helicopter = entity_settings["speed_helicopter"]
        self.speed_truck = entity_settings["speed_truck"]
        self.direction_truck = Rect(0, 0, 1, 1)
        self.truck_tank_max = entity_settings["speed_truck"]
        self.truck_tank_actual = 0                                  # todo
        self.mineral_truck = False
        self.mineral_mine = 0
        self.mineral_mine_start = 0
        self.mineral_fabric = 0
        self.mineral_fabric_start = 0
        self.game_over = False