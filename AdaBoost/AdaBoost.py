__author__ = 'luoming'
import math

class Point:
    def __init__(self, x, y, classType):
        self.x = x
        self.y = y
        self.classType = classType
        self.probably = 0.0

CLASS_POSITIVE = 1
CLASS_NEGATIVE = -1
CLASSIFICATION = ['X=2.5', 'X=7.5', 'Y=5.5']

def readDataFile(filePath):
    data = []
    totalPoint = []
    f = open(filePath, 'rU')
    for line in f:
        line = line.strip()
        tmp = line.split()
        data.append(tmp)
#    print data
    for array in data:
        point = Point(int(array[0]), int(array[1]), int(array[2]))
        point.probably = 1.0/len(data)
        totalPoint.append(point)
    return totalPoint

def calculateWeight(errorValue):
    temp = (1-errorValue) / errorValue
    alpha = 0.5 * math.log(temp, math.e)
    return alpha

def dataNormalized(totalPoint):
    sumProbably = 0.0
    for point in totalPoint:
        sumProbably += point.probably
    for point in totalPoint:
        temp = point.probably
        point.probably = temp / sumProbably

def calculateErrorValue(pointMap):
    resultValue = 0.0
    for key in pointMap:
        pList = pointMap[key]
        for p in pList:
            if key != p.classType:
                resultValue += p.probably
    weight = calculateWeight(resultValue)
    for key in pointMap:
        pList = pointMap[key]
        for p in pList:
            prob = p.probably
            if key != p.classType:
                p.probably = prob * math.exp(weight)
            else:
                p.probably = prob * math.exp(-1 * weight)
    return resultValue

def classifyData(totalPoint, classification, point):
    isLarger = False
    posProbably = 0
    negProbably = 0
    pList = []
    array = classification.split('=')
    position = array[0]
    value = float(array[1])
    if position == 'X':
        if point.x > value:
            isLarger = True
        for data in totalPoint:
            if isLarger and data.x > value:
                pList.append(data)
            elif not isLarger and data.x < value:
                pList.append(data)
    elif position == 'Y':
        if point.y > value:
            isLarger = True
        for data in totalPoint:
            if isLarger and data.y > value:
                pList.append(data)
            elif not isLarger and data.y < value:
                pList.append(data)
    for p in pList:
        if p.classType == CLASS_POSITIVE:
            posProbably += 1
        else:
            negProbably += 1

    if posProbably > negProbably:
        return CLASS_POSITIVE
    else:
        return CLASS_NEGATIVE

def calculateWeightArray(totalPoint):

    mapList = {}
    CLASSIFICATION_WEIGHT = []
    for i in range(len(CLASSIFICATION)):
        posPointList = []
        negPointList = []
        for p in totalPoint:
            tempClassType = classifyData(totalPoint, CLASSIFICATION[i], p)
            if tempClassType == CLASS_POSITIVE:
                posPointList.append(p)
            else:
                negPointList.append(p)
        mapList[CLASS_POSITIVE] = posPointList
        mapList[CLASS_NEGATIVE] = negPointList
        errorValue = calculateErrorValue(mapList)
        dataNormalized(totalPoint)
        CLASSIFICATION_WEIGHT.append(calculateWeight(errorValue))
    return CLASSIFICATION_WEIGHT

def adaBoostClassify(totalPoint):
    classifyWeight = calculateWeightArray(totalPoint)
    for i in range(len(CLASSIFICATION)):
        print 'classifier [%d]  weight [%f]' % ((i+1), classifyWeight[i])
    for j in range(len(totalPoint)):
        point = totalPoint[j]
        value = 0.0
        for i in range(len(CLASSIFICATION)):
            value += 1.0 * classifyData(totalPoint, CLASSIFICATION[i], point) * classifyWeight[i]
        if value > 0:
            print 'point(%d, %d) combination classify is 1, the really Classify is %d' % (point.x, point.y, point.classType)
        else:
            print 'point(%d, %d) combination classify is -1, the really Classify is %d' % (point.x, point.y, point.classType)



if __name__ == '__main__':
    totalPoint = readDataFile('AdaBoost_input.txt')
    adaBoostClassify(totalPoint)

