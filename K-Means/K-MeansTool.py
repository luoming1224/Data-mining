__author__ = '25691'
import Point
import math

class KMeansTool :
    def __init__(self, filePath, classNum):
        self.filePath = filePath
        self.classNum = classNum
        self.classNames = []
        self.classPoints = []
        self.totalPoints = []
        self.readDataFile()

    def readDataFile(self):
        f = open(self.filePath, 'rU')
        dataList = []
        for line in f:
            tmp = line.split()
            dataList.append(tmp)
        print dataList

        size = len(dataList)
        for i in range(0, size):
            if i < self.classNum:
                tmpoint = Point.Point(float(dataList[i][0]), float(dataList[i][1]), i+1)
                self.classPoints.append(tmpoint)
                self.classNames.append(i+1)
            tmpoint = Point.Point(float(dataList[i][0]), float(dataList[i][1]))
            self.totalPoints.append(tmpoint)

    def kMeansClustering(self):
        error = 99999
        while error > 0.01 * self.classNum:
            for p1 in self.totalPoints:
                for p2 in self.classPoints:
                    p2.computeDistance(p1)
#                for i in range(0, len(self.classPoints)):
#                    print self.classPoints[i].distance,
#                    print self.classPoints[i].className,
#                print
                self.classPoints.sort(cmp=None, key=lambda x: x.distance, reverse=False)
#                for i in range(0, len(self.classPoints)):
#                    print self.classPoints[i].distance,
#                    print self.classPoints[i].className,
#                print
                p1.className = self.classPoints[0].className
#                print p1.className
#            for i in range(0, len(self.totalPoints)):
#                print self.totalPoints[i].x, self.totalPoints[i].y, self.totalPoints[i].className, self.totalPoints[i].distance
#            for j in range(0, len(self.classPoints)):
#                print self.classPoints[j].className

            error = 0
            for p1 in self.classPoints:
                tempX = 0
                tempY = 0
                count = 0
                for p in self.totalPoints:
                    if p.className == p1.className:
                        count += 1
                        tempX += p.x
                        tempY += p.y
                tempX /= count
                tempY /= count

                error += math.fabs(tempX - p1.x)
                error += math.fabs(tempY - p1.y)

                p1.x = tempX
                p1.y = tempY

            for i in range(0, len(self.classPoints)):
                temp = self.classPoints[i]
                print 'cluster center: ', i+1, ' x=', temp.x, ' y=', temp.y

            print '---------------'

        print 'result:'
        for i in range(0, len(self.classPoints)):
            temp = self.classPoints[i]
            print 'cluster center: ', i+1, ' x=', temp.x, ' y=', temp.y



if __name__ == '__main__':
    filePath = r'input.txt'
    kMeans = KMeansTool(filePath, 3)
    kMeans.kMeansClustering()
