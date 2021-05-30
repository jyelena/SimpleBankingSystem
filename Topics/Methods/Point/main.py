import math

class Point:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def dist(self, a_point):
        return math.sqrt((self.x - a_point.x) ** 2 + (self.y - a_point.y) ** 2)
