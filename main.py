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

    def countNeighbours(self, houseCoordinates, lastCoor, k):
        countToRemove = 0
        countToAdd = 0
        costToAdd = 0
        costToRemove = 0
        if lastCoor[0] == self.x and lastCoor[1] == self.y:
            startTime = time.time()
            self.countSquare(0, self.x + k + 1, houseCoordinates, k)
            endTime = time.time()
            print("first element:", (endTime - startTime)
                  * 1000, "ms", self.x, self.y)
        else:
            if lastCoor[0] != self.x:
                # print("new-line")
                self.countSquare(max(
                    0, self.x - k), min(len(houseCoordinates), self.x + k + 1), houseCoordinates, k)
            else:
                if self.y - lastCoor[1] > k:
                    startTime = time.time()
                    self.countSquare(max(0, self.x - k),
                                     min(len(houseCoordinates), self.x + k + 1), houseCoordinates, k)
                    endTime = time.time()
                    #print("count square:", (endTime - startTime)*1000, "ms")
                else:
                    startY01 = max(0, lastCoor[1] - k)
                    endY01 = max(0, self.y - k)

                    startY02 = min(16384, lastCoor[1] + k + 1)
                    endY02 = min(16384, self.y + k + 1)

                    startX = max(0, self.x - k)
                    endX = min(len(houseCoordinates), self.x + k + 1)

                    startTime = time.time()
                    if startY01 != endY01:
                        for row in range(startX, endX):
                            for j in range(startY01, endY01):
                                if j in houseCoordinates[row]:
                                    countToRemove += 1
                                    costToRemove += houseCoordinates[row][j].price
                    endTime = time.time()
                    print("time to remove:", (endTime - startTime)*1000, "ms")
                    startTime = time.time()
                    for row in range(startX, endX):
                        for j in range(startY02, endY02):
                            if j in houseCoordinates[row]:
                                countToAdd += 1
                                costToAdd += houseCoordinates[row][j].price
                    endTime = time.time()
                    print("time to add:", (endTime - startTime)*1000, "ms")
                    self.numberOfNeighbours = max(
                        0, houseCoordinates[lastCoor[0]][lastCoor[1]].numberOfNeighbours - countToRemove + countToAdd)
                    self.costOfNeighbours = max(
                        0, houseCoordinates[lastCoor[0]][lastCoor[1]].costOfNeighbours - costToRemove + costToAdd)
        # print(self.numberOfNeighbours)
        return [self.x, self.y]

    def countSquare(self, startX, endX, houseCoordinates, k):
        startY = max(0, self.y - k)
        endY = self.y + k
        for row in range(startX, endX):
            for j in houseCoordinates[row]:
                if j >= startY:
                    if j <= endY:
                        self.numberOfNeighbours += 1
                        self.costOfNeighbours += houseCoordinates[row][j].price
                    else:
                        break


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
    f = open("test02.txt", "r")
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
    numberRows = len(mapa)
    numberCollumns = len(mapa[0])

    for i in range(numberRows):
        #startTime01 = time.time()
        houseCoordinates[i] = {}
        for j in range(numberCollumns):
            if mapa[i][j] != 0:
                houseCoordinates[i][j] = House(i, j, mapa[i][j])
        #endTime01 = time.time()
        #print("finished line init:", (endTime01 - startTime01)*1000, "ms")

    endTime = time.time()
    print("finished dict init:", (endTime - startTime)*1000, "ms")

    print('starting algorithm')
    startTime = time.time()
    countOfN = []
    k = 500
    for i in range(numberRows):
        print(i)
        countOfN.append([])
        for j in range(numberCollumns):
            countOfN[i].append(0)
            if j == 0:
                for y in range(k + 1):
                    if mapa[i][y] != 0:
                        countOfN[i][0] += 1
            else:
                if j < numberCollumns - k:
                    if mapa[i][j + k] != 0:
                        countOfN[i][j] = countOfN[i][j - 1] + 1
                if j > k:
                    if mapa[i][j - k - 1] != 0:
                        countOfN[i][j] = countOfN[i][j - 1] - 1

    endTime = time.time()
    print("alternate:", (endTime - startTime)*1000, "ms")

    countCoveregeOfHouses(houseCoordinates)
    return count


def countCoveregeOfHouses(houseCoordinates):

    i = 0
    timeOnLine = 0

    for x in range(1):
        startTime = time.time()
        for y in houseCoordinates[0]:
            if i == 0:
                lastCoor = [0, y]
            lastCoor = houseCoordinates[0][y].countNeighbours(
                houseCoordinates, lastCoor, 500)

            i += 1
        endTime = time.time()
        print("line done in:", (endTime - startTime)*1000)
        timeOnLine += (endTime - startTime)*1000

    print("avarage time per line:", timeOnLine/16384)

# def goOverHouses():


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
print(result)


# saveOutput(outputContent)
endTime = time.time()
print("done main in", (endTime - startTime)*1000, "ms")
