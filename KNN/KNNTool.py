__author__ = '25691'
import Sample

class KNNTool:
    def __init__(self, trainDataPath, testDataPath):
        self.trainDataPath = trainDataPath
        self.testDataPath = testDataPath
        self.classWeightTuple = (1, 1, 1, 1)
        self.classTypes = []
        self.resultSamples = []
        self.trainSamples = []
        self.trainData = []
        self.testData = []
        self.readDataFromFile()

    def readDataFromFile(self):
        self.trainData = self.fileDataToList(self.trainDataPath)
        tmp = {}
        for s in self.trainData:
            tmp[s[0]] = 0
        self.classTypes = tmp.keys()

        self.testData = self.fileDataToList(self.testDataPath)

    def fileDataToList(self, filePath):
        Data = []
        f = open(filePath, 'rU')
        for line in f:
            tmp = line.split()
            Data.append(tmp)
        f.close()
        return Data

    def computeEuclideanDistance(self, s1, s2):
        f1 = s1.getFeatures()
        f2 = s2.getFeatures()
        distance = 0
        length = len(f1)
        for i in range(0, length):
            subF1 = int(f1[i])
            subF2 = int(f2[i])
            distance += (subF1 - subF2) * (subF1 - subF2)
        return distance

    def knnCompute(self, k):
        resultSamples = []
        trainSamples = []
        classWeight = {}
        for s in self.testData:
            temp = Sample.Sample(s)
            resultSamples.append(temp)

        for s in self.trainData:
            className = s[0]
            tempF = s[1:]
            temp = Sample.Sample(tempF, className)
            trainSamples.append(temp)


        for s in resultSamples:
            classCount = {}
            index = 0
            for type in self.classTypes:
                classCount[type] = 0
                classWeight[type] = self.classWeightTuple[index]
                index += 1

            for tS in trainSamples:
                dis = self.computeEuclideanDistance(s, tS)
                tS.setDistance(dis)
#                print tS.getClassName(), ':', dis,
#            print

            trainSamples.sort(cmp=None, key=lambda x:x.getDistance(), reverse=False)

#            for t in trainSamples:
#                print t.getClassName(), ':', t.getDistance(),
#            print

            kNNSample = []
            for i in range(0, len(trainSamples)):
                if i < k:
                    kNNSample.append(trainSamples[i])
                else:
                    break

            for s1 in kNNSample:
                num = classCount[s1.getClassName()]
                num += classWeight[s1.getClassName()]
                classCount[s1.getClassName()] = num
#            print classCount.keys()
#            print classCount.items()

            maxCount = 0
            index = 0
            for entry in classCount.values():
                if entry > maxCount:
                    maxCount = entry
                    s.setClassName(classCount.keys()[index])
                index += 1

#            print 'Test data classification:'
            print s.getFeatures(), ' classify:', s.getClassName()






if __name__ == '__main__':
    trainDataPath = r'trainData.txt'
    testDataPath = r'testData.txt'

    knn = KNNTool(trainDataPath, testDataPath)
    knn.knnCompute(3)
