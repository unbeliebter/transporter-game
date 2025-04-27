from src.baseEntity import BaseEntity

# Klasse für den LKW
class Vehicle(BaseEntity):
    act_tank = 0
    max_tank = 100
    tank_loss = 0.1
    has_mineral = False
    heading = "Stehend"

    def __init__(self, act_tank, max_tank, has_mineral, tank_loss, width, height, pos_x, pos_y, image_path):
        super().__init__(width, height, pos_x, pos_y, image_path)
        self.act_tank = act_tank
        self.max_tank = max_tank
        self.has_mineral = has_mineral
        self.tank_loss = tank_loss
