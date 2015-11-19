__author__ = '25691'

class Sample :
    def __init__(self, features, className = None):
        self.distance = 0
        self.features = features
        self.className = className
    def getClassName(self):
        return self.className
    def setClassName(self, className):
        self.className = className
    def getFeatures(self):
        return self.features
    def setFeatures(self, features):
        self.features = features
    def getDistance(self):
        return self.distance
    def setDistance(self, distance):
        self.distance = distance