from src.baseEntity import BaseEntity

# Ist eine zusätzliche Klasse, um zu Erfassen für die Mine und die Fabrik wie viele Mineralien diese haben und Benötigen
# Die Klasse ansich erbt von BaseEntity
class Counter(BaseEntity):
    max_items = 0
    act_items = 0

    def __init__(self, max_items, act_items, width, height, pos_x, pos_y, image_path):
        super().__init__(width, height, pos_x, pos_y, image_path)
        self.max_items = max_items
        self.act_items = act_items