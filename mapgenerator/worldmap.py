__author__ = 'Siarshai'


class WorldMap:
    # Пока что только высота
    def __init__(self, x_dots, y_dots):
        self.x_dots = x_dots
        self.y_dots = y_dots
        self.world_map = [[0]*self.x_dots for i in range(self.y_dots)]