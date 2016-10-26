import math
import operator
import csv
from random import shuffle

sigma = 0.97

def preprocessData(filePath):
    rownum = 0
    all = []
    normalized = []
    colMin = []
    colMax = []
    maxMinDiff = []

    with open(filePath, 'rU') as file:
        reader = csv.reader(file)
        for row in reader:
            if rownum is 0:
                header = row
                rownum += 1
            else:
                all.append(row)
    shuffle(all)
    xColCount = len(all[0]) - 1

    # finding max, min, and difference of max & min for each column
    for i in range(0, xColCount):
        colMin.append(float(min(row[i] for row in all)))
        colMax.append(float(max(row[i] for row in all)))
        maxMinDiff.append(float(colMax[i]) - float(colMin[i]))

    # normalizing using (value - min)/(max - min)
    length = len(all[0]) - 1
    for i in range(0, len(all)):
        temp = []
        for j in range(0, length):
            temp.append(round(((float(all[i][j]) - colMin[j]) / maxMinDiff[j]), 2))
        temp.append(all[i][-1])
        normalized.append(temp)
    return normalized

def feedInput(allInstances, k, kn):
    foldLength = len(allInstances) / k

    for distanceType in range(1, 4):
        gCount = foldLength  # first foldLength number of instances are test instances
        foldAccuracy = []
        testingSet = allInstances[0:foldLength]

        for i in range(k - 1):
            #making training folds
            j = 0
            trainingSet = []
            while j < foldLength and gCount < len(allInstances):
                trainingSet.append(allInstances[gCount])
                gCount += 1
                j += 1
            #getting predictions
            predictedClass = []
            for x in range(foldLength):
                neighbors = getNeighbors(trainingSet, testingSet[x], kn, distanceType)
                predictedClass.append(getResponse(neighbors))
            foldAccuracy.append(getAccuracy(testingSet, predictedClass))
        #print foldAccuracy
        cummulativeAccuracy = 0
        for i in range(len(foldAccuracy)):
            cummulativeAccuracy += foldAccuracy[i]
        print 'Accuracy for distanceType: ' + str(distanceType)
        print cummulativeAccuracy/len(foldAccuracy)

def eucledianDistance(row1, row2, length):
    distance = 0
    for i in range(0, length):
        distance += pow((float(row1[i]) - float(row2[i])), 2)
    return math.sqrt(distance)

def polynomialKernel(row1, row2, length):
    p = 3
    k_xy = pow((1 + dotProduct(row1, row2, length)), p)
    k_xx = pow((1 + dotProduct(row1, row1, length)), p)
    k_yy = pow((1 + dotProduct(row2, row2, length)), p)
    distance = math.sqrt(k_xx - (2 * k_xy) + k_yy)
    return distance

def dotProduct(row1, row2, length):
    product = 0
    for i in range(length):
        product += (row1[i] * row2[i])
    return product

def calculateKXY(row1, row2, length):
    global sigma
    return math.exp(-pow(eucledianDistance(row1, row2, length), 2) / pow(sigma, 2))

def radialKernel(row1, row2, length):
    k_xx = calculateKXY(row1, row1, length)
    k_xy = calculateKXY(row1, row2, length)
    k_yy = calculateKXY(row2, row2, length)
    distance = math.sqrt(k_xx - (2 * k_xy) + k_yy)
    return distance

def getNeighbors(trainingSet, testingInstance, k, distanceType):
    distances = []
    instanceLength = len(testingInstance) - 1
    length = len(trainingSet)
    for i in range(0, length):
        if distanceType == 1:
            d = eucledianDistance(trainingSet[i], testingInstance, instanceLength)
        else:
            if distanceType == 2:
                d = polynomialKernel(trainingSet[i], testingInstance, instanceLength)
            else:
                if distanceType == 3:
                    d = radialKernel(trainingSet[i], testingInstance, instanceLength)
                else:
                    print 'Incorrect distance type.'
                    return

        distances.append((trainingSet[i], d))
    distances.sort(key = operator.itemgetter(1))

    neighbors = []
    if len(distances) < k:
        for i in range(len(distances)):
            neighbors.append(distances[i][0])
    else:
        for i in range(k):
            neighbors.append(distances[i][0])
    return neighbors

def getResponse(neighbors):
    votes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in votes:
            votes[response] += 1
        else:
            votes[response] = 1
    sortedVotes = sorted(votes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def getAccuracy(testSet, predictions):

    correct = 0
    for x in range(len(testSet)):
        print testSet[x], predictions[x]
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0


fileOption = input("Enter 1 for Ecoli, 2 for Glass and 3 for Yeast dataset: ")
#distanceType = input("Enter 1 for Euclidean Distance, 2 for Polynomial Kernel and 3 for Radial based: ")
k = input("Enter k, the fold count: ")
kn = input("Enter kn, the neighbor count: ")

allInstances = []
if fileOption == 1:
    allInstances = preprocessData('/Users/niraj/Desktop/ML_6363/A2/ecoli.csv')
else:
    if fileOption == 2:
        allInstances = preprocessData('/Users/niraj/Desktop/ML_6363/A2/glass.csv')
    else:
        if fileOption == 3:
            allInstances = preprocessData('/Users/niraj/Desktop/ML_6363/A2/yeast.csv')
        else:
            print 'Incorrect option chosen.'
feedInput(allInstances, k, kn)