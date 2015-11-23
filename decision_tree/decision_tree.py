__author__ = 'luoming'
from math import log
from copy import copy

attrname = []
data = []

def readData(filePath):
    global attrname
    datat = []
    f = open(filePath, 'rU')
    for line in f:
        tmp = line.split()
        tmp = tmp[1:]
        datat.append(tmp)
    attrname = datat[0]
    data = datat[1:]
#    print attrname
#    print data
    return data , attrname

def calcEntropy(dataset):
    numEntries = len(dataset)
    labelCounts = {}
    for featVec in dataset:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    Entropy = 0.0
    for key in labelCounts.keys():
        prob = float(labelCounts[key])/numEntries
        Entropy -= prob * log(prob, 2)
    return  Entropy

def splitDataSet(dataset, axis, value):
    retDataSet = []
    for featVec in dataset:
        if featVec[axis] == value:
            remainFeatVec = featVec[:axis]
            remainFeatVec.extend(featVec[axis+1:])
            retDataSet.append(remainFeatVec)
    return retDataSet

def chooseBestFeature(dataset):
    numFeatures = len(dataset[0])-1
    baseEntropy = calcEntropy(dataset)
    bestInfoGain = 0.0;bestFeature = -1;bestindex = 0
    for i in range(numFeatures):
        featList = [example[i] for example in dataset]
        uniqueVals = set(featList)
        newEntropy = 0.0
        splitInformation = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataset, i, value)
            prob = len(subDataSet)/float(len(dataset))
            splitInformation -= prob * log(prob, 2)
            newEntropy += prob * calcEntropy(subDataSet)
        infoGain = baseEntropy - newEntropy      #ID3
        GainRatio = infoGain / splitInformation  #C4.5
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = attrname[i]
            bestindex = i
    return bestindex

def createTree(dataset):
    classList = [example[-1] for example in dataset]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    bestindex = chooseBestFeature(dataset)
    bestFeatLabel = attrname[bestindex]
    myTree = {bestFeatLabel:{}}
    del(attrname[bestindex])
    featValues = [example[bestindex] for example in dataset]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataset, bestindex, value))
    return myTree

def classify(inputTree, labels, testdata):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = labels.index(firstStr)
    for key in secondDict.keys():
        if testdata[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], labels, testdata)
            else:
                classLabel = secondDict[key]
    return classLabel





if __name__ == '__main__':
    filePath = r'decisiontree_input.txt'
    data, attr = readData(filePath)
#    print calcEntropy(data)
#    print chooseBestFeature(data)
    label = copy(attr)
    myTree = createTree(data)
    testdata = ['Sunny', 'Cool', 'Normal', 'Weak']
    classLabel = classify(myTree, label, testdata)
    print classLabel