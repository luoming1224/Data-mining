__author__ = '25691'
from math import hypot

class Point:
    def __init__(self, x, y, className = None):
        self.x = x
        self.y = y
        self.className = className
        self.distance = 0

    def computeDistance(self, p):
        self.distance = hypot((self.x - p.x), (self.y - p.y))
 #       self.distance = (self.x - p.x) * (self.x - p.x) + (self.y - p.y) * (self.y - p.y)


if __name__ == '__main__':
    point1 = Point(5.02, 4.01)
    point2 = Point(4.01, 3.00)
    point1.computeDistance(point2)
    print point1.distance
