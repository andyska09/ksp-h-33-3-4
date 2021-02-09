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

    def countNeighbours(self, houseCoordinates, lastCoor):
        countToRemove = 0
        countToAdd = 0
        if lastCoor[0] == self.x and lastCoor[1] == self.y:
            for row in range(0, 501):
                if not(row in houseCoordinates):
                    break
                for j in houseCoordinates[row]:
                    if not(row == 0 and j == 0):
                        self.numberOfNeighbours += 1
        else:
            startX01 = 0
            endX01 = 0
            if (self.x - 500 >= 0) and (lastCoor[0] - 500 >= 0):
                startX01 = self.x - 500
                endX01 = self.x - 500 + (self.x - lastCoor[0])

            startX02 = lastCoor[0] + 500
            endX02 = self.x + 500
            if lastCoor[0] + 500 >= len(houseCoordinates) - 1:
                startX02 = len(houseCoordinates) - 1
                endX02 = len(houseCoordinates) - 1

            startY01 = 0
            endY01 = 0
            if self.y - 500 < 0:
                if lastCoor[1] > self.y:
                    startY01 = 0
                    endY01 = 0
            elif (self.y - 500 >= 0) and (lastCoor[1] - 500 >= 0):
                startY01 = self.y - 500
                endX01 = self.x - 500 + (self.x - lastCoor[0])

            startY02 = lastCoor[1] + 500
            endY02 = self.y + 500
            if lastCoor[1] + 500 >= len(houseCoordinates[0]) - 1:
                startY02 = len(houseCoordinates[0]) - 1
                endY02 = len(houseCoordinates[0]) - 1

            for row in range(startX01, endX01):
                if not(row in houseCoordinates):
                    break
                for j in range(startY01, endY01):
                    if j in houseCoordinates[row]:
                        countToRemove += 1
            for row in range(startX02, endX02):
                if not(row in houseCoordinates):
                    break
                for j in range(startY02, endY02):
                    if j in houseCoordinates[row]:
                        countToAdd += 1

            self.numberOfNeighbours = houseCoordinates[lastCoor[0]
                                                       ][lastCoor[1]].numberOfNeighbours - countToRemove + countToAdd
        return [self.x, self.y]


def init():
    S = 16384
    mapa = []
    with open("/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/01.in", "rb") as input_file:
        for y in range(S):
            numpy_radek = numpy.fromfile(
                input_file,
                dtype="<u2",
                count=S
            )
            radek = array('H')
            radek.fromlist(numpy_radek.tolist())
            mapa.append(radek)
    return mapa


def initTest():
    f = open("test.txt", "r")
    mapa = []
    for i in f:
        mapa.append([i])
    for i in range(len(mapa)):
        mapa[i] = numpy.array(list(map(int, mapa[i][0].split())))
    return mapa


def createTestMap(start, end):
    mapa = init()
    newMap = []
    x = 0
    for i in range(start[0], end[0]):
        newMap.append([])
        for j in range(start[1], end[1]):
            newMap[x].append(mapa[i][j])
        x += 1

    result = []
    for i in range(len(newMap)):
        for j in range(len(newMap[0])):
            newMap[i][j] = str(newMap[i][j])

    for i in range(len(newMap)):
        result.append(" ".join(newMap[i]))

    outputContent = "\n".join(result)
    print("saving test map to file:", "\n", outputContent)

    f = open("test.txt", "w")
    f.write(outputContent)
    f.close()
    return


def saveOutput(outputContent):
    savePath = "/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/ksp-h-210221-04-py/outputs"
    name = datetime.now().strftime("%y%m%d-%H-%M-%S")
    completeName = os.path.join(savePath, name+"-out.txt")
    f = open(completeName, "w")
    f.write(outputContent)
    f.close()


def main(mapa):
    count = 0
    houseCoordinates = {}
    for i in range(len(mapa)):
        houseCoordinates[i] = {}
        for j in range(len(mapa[0])):
            if mapa[i][j] != 0:
                houseCoordinates[i][j] = House(i, j, mapa[i][j])
    print('starting algorithm')
    countCoveregeOfHouses(houseCoordinates)
    return count


def countCoveregeOfHouses(houseCoordinates):
    startTime = time.time()
    lastCoor = [0, 8260]
    for x in houseCoordinates:
        for y in houseCoordinates[x]:
            lastCoor = houseCoordinates[x][y].countNeighbours(
                houseCoordinates, lastCoor)
    endTime = time.time()
    print("done first line in", (endTime - startTime)*1000, "ms")


print("start")
startTime = time.time()

mapa = init()
#createTestMap([11, 12356], [26, 12376])
#mapa = initTest()

endTime = time.time()
print("done init in:", (endTime - startTime)*1000, "ms")

startTime = time.time()
# print(mapa)

result = main(mapa)
mapa = []
print(result)


# saveOutput(outputContent)
endTime = time.time()
print("done main in", (endTime - startTime)*1000, "ms")
