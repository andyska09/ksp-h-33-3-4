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

    def countNeighbours(self, houseCoordinates, lastCoor, k):
        countToRemove = 0
        countToAdd = 0
        if lastCoor[0] == self.x and lastCoor[1] == self.y:
            startTime = time.time()
            for row in range(0, self.x + k + 1):
                for j in houseCoordinates[row]:
                    if j != self.y or row != self.x:
                        if j <= self.y + k:
                            self.numberOfNeighbours += 1
                        else:
                            break
            endTime = time.time()
            print("first element:", (endTime - startTime)
                  * 1000, "ms", self.x, self.y)
        else:
            if lastCoor[0] != self.x:
                print("new-line")
                for row in range(max(0, self.x - k), min(len(houseCoordinates) - 1, self.x + k + 1)):
                    for j in houseCoordinates[row]:
                        if j != self.y or row != self.x:
                            if j <= self.y + k:
                                self.numberOfNeighbours += 1
                            else:
                                break
            else:
                startY01 = max(0, self.y - k - 1)
                endY01 = max(0, self.y - k)
                startY02 = lastCoor[1] + k + 1
                endY02 = self.y + k + 1

                startX = max(0, self.x - k)
                endX = min(len(houseCoordinates) - 1, self.x + k + 1)

                startTime = time.time()
                if startY01 != endY01:
                    for row in range(startX, endX):
                        if startY01 in houseCoordinates[row]:
                            countToRemove += 1
                        if startY02 in houseCoordinates[row]:
                            countToAdd += 1
                else:
                    for row in range(startX, endX):
                        if startY02 in houseCoordinates[row]:
                            countToAdd += 1

                endTime = time.time()
                #print("second element:", (endTime - startTime)*1000, "ms")
                self.numberOfNeighbours = houseCoordinates[lastCoor[0]
                                                           ][lastCoor[1]].numberOfNeighbours - countToRemove + countToAdd
        print(self.numberOfNeighbours)
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
    startTime = time.time()
    for i in range(len(mapa)):
        houseCoordinates[i] = {}
        for j in range(len(mapa[0])):
            if mapa[i][j] != 0:
                houseCoordinates[i][j] = House(i, j, mapa[i][j])

    endTime = time.time()
    print("finished dict init:", (endTime - startTime)*1000, "ms")

    print('starting algorithm')
    #startTime = time.time()
    # for y in houseCoordinates[0]:
    #    count += houseCoordinates[0][y].price
    ##endTime = time.time()
    #print("first element:", (endTime - startTime)*1000, "ms")

    countCoveregeOfHouses(houseCoordinates)
    return count


def countCoveregeOfHouses(houseCoordinates):

    i = 0
    timeLine = 0

    for x in houseCoordinates:
        startTime = time.time()
        if i > 4000:
            break
        for y in houseCoordinates[x]:
            if i == 0:
                lastCoor = [x, y]
            lastCoor = houseCoordinates[x][y].countNeighbours(
                houseCoordinates, lastCoor, 500)
            i += 1
        endTime = time.time()
        timeLine += (endTime - startTime)*1000

    print("avarage time per line:", timeLine/4001)


print("start")
startTime = time.time()

mapa = init()
# createTestMap([11, 12356], [26, 12376])
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
