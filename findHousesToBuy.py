import os
import numpy
import time
from datetime import datetime
from array import array


class House:
    def __init__(self, x, y, price):
        self.x = x
        self.y = y
        self.price = price
        self.numberOfNeighbours = 0
        self.costOfNeighbours = 0
        self.isCovered = False

    def updateCoverage(self, houseCoordinates, k):
        self.isCovered = True
        startX = max(0, self.x - k)
        endX = min(len(houseCoordinates), self.x + k + 1)
        startY = max(0, self.y - k)
        endY = self.y + k
        for row in range(startX, endX):
            for j in houseCoordinates[row]:
                if j >= startY:
                    if j <= endY:
                        houseCoordinates[row][j].isCovered = True
                    else:
                        break


def findHousesToBuy(houseCoordinates, k):
    #housesToBuy = []
    print("start search")
    maxCoor = findMax(houseCoordinates)
    # for i in range(10000):
    #    print(i)

    #    if maxCoor[0] == -1:
    #        print("ended before 10,000")
    #        break
    #    houseCoordinates[maxCoor[0]][maxCoor[1]].updateCoverage(houseCoordinates, k)
    #    housesToBuy.append(maxCoor)
    return houseCoordinates[maxCoor[0]][maxCoor[1]]


def findMax(houseCoordinates):
    maximum = 0
    maxCoor = [-1, -1]
    startTime = time.time()
    for i in houseCoordinates:
        for j in houseCoordinates[i]:
            if not houseCoordinates[i][j].isCovered:
                if maximum < houseCoordinates[i][j].x:
                    maximum = houseCoordinates[i][j].x
                    maxCoor = [i, j]
    endTime = time.time()
    print("found Max:", (endTime - startTime)*1000, "ms")
    return maxCoor


def readSavedDict():
    f = open("/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/ksp-h-210221-04-py/outputs/210215-20-29-52-out.txt", "r")
    houseCoordinates = {}
    for i in f:
        line = list(map(int, i.split(" ")))
        # print(line)
        houseCoordinates[(line[0], line[1])] = House(
            line[0], line[1], line[2])
    return houseCoordinates


def saveOutput(outputContent):
    savePath = "/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/ksp-h-210221-04-py/outputs"
    name = datetime.now().strftime("%y%m%d-%H-%M-%S")
    completeName = os.path.join(savePath, name+"-out.txt")
    f = open(completeName, "w")
    f.write(outputContent)
    f.close()


print("start")
startTime = time.time()

houseCoor = readSavedDict()

endTime = time.time()
print("done init in:", (endTime - startTime)*1000, "ms")

startTime = time.time()

#outputContent = formatResult(result)


# saveOutput(outputContent)
endTime = time.time()
print("done main in", (endTime - startTime)*1000, "ms")
