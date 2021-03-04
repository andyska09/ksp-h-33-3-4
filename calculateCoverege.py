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


def main(mapa, k):
    print('starting algorithm')
    houseCoordinates = countCoveregeOfHouses(mapa, k)
    return houseCoordinates


def countCoveregeOfHouses(mapa, k):
    numberRows = len(mapa)
    numberCollumns = len(mapa[0])
    houseCoordinates = {}

    startTime = time.time()
    countOfNRow = []
    costOfNRow = []
    for i in range(numberRows):
        # print(i)
        houseCoordinates[i] = {}
        countOfNRow.append([])
        costOfNRow.append([])
        for j in range(numberCollumns):
            countOfNRow[i].append(0)
            costOfNRow[i].append(0)
            if mapa[i][j] != 0:
                houseCoordinates[i][j] = House(i, j, mapa[i][j])
            if j == 0:
                for y in range(k + 1):
                    if mapa[i][y] != 0:
                        countOfNRow[i][0] += 1
                        costOfNRow[i][0] += mapa[i][y]
            else:
                countOfNRow[i][j] = countOfNRow[i][j - 1]
                costOfNRow[i][j] = costOfNRow[i][j - 1]
                if j < numberCollumns - k:
                    if mapa[i][j + k] != 0:
                        countOfNRow[i][j] += 1
                        costOfNRow[i][j] += mapa[i][j + k]

                if j > k:
                    if mapa[i][j - k - 1] != 0:
                        countOfNRow[i][j] -= 1
                        costOfNRow[i][j] -= mapa[i][j - k - 1]

    endTime = time.time()
    print("first part:", (endTime - startTime)*1000, "ms")

    startTime = time.time()
    countOfN = []
    costOfN = []
    for i in range(numberRows):
        print(i)
        countOfN.append([])
        costOfN.append([])
        for j in range(numberCollumns):
            countOfN[i].append(0)
            costOfN[i].append(0)
            if i == 0:
                for y in range(max(0, i - k), min(numberRows, i + k + 1)):
                    countOfN[i][j] += countOfNRow[y][j]
                    costOfN[i][j] += costOfNRow[y][j]
            else:
                countOfN[i][j] = countOfN[i - 1][j]
                costOfN[i][j] = costOfN[i - 1][j]
                if i < numberRows - k:
                    countOfN[i][j] += countOfNRow[i + k][j]
                    costOfN[i][j] += costOfNRow[i + k][j]
                if i > k:
                    countOfN[i][j] -= countOfNRow[i - k - 1][j]
                    costOfN[i][j] = max(0, costOfN[i]
                                        [j] - costOfNRow[i - k - 1][j])
            if mapa[i][j] != 0:
                if i in houseCoordinates:
                    if j in houseCoordinates[i]:
                        houseCoordinates[i][j].numberOfNeighbours = countOfN[i][j]
                        houseCoordinates[i][j].costOfNeighbours = costOfN[i][j]
    endTime = time.time()
    print("second part:", (endTime - startTime)*1000, "ms")
    return houseCoordinates


def formatResult(result):
    out = ""
    for i in result:
        for j in result[i]:
            house = result[i][j]
            out += str(i) + " " + str(j) + " " + str(house.price) + " " + str(
                house.numberOfNeighbours) + " " + str(house.costOfNeighbours) + "\n"
    return out


print("start")
startTime = time.time()

#mapa = init()
# createTestMap([11, 12356], [26, 12376])
mapa = initTest()

endTime = time.time()
print("done init in:", (endTime - startTime)*1000, "ms")

startTime = time.time()

result = main(mapa, 2)
# print(result)
outputContent = formatResult(result)


saveOutput(outputContent)
endTime = time.time()
print("done main in", (endTime - startTime)*1000, "ms")
