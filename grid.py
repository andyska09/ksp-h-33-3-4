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
    f = open("test03.txt", "r")
    mapa = []
    for i in f:
        mapa.append([i])
    for i in range(len(mapa)):
        mapa[i] = numpy.array(list(map(int, mapa[i][0].split())))
    return mapa


def main(mapa, loadedInput, k):
    print('starting algorithm')
    numberRows = len(mapa)
    numberCollumns = len(mapa[0])
    houseCoor = {}
    for x in range(numberRows):
        for y in range(numberCollumns):
            housePrice = mapa[x][y]
            cell = (x // (k + 1), y // (k + 1))

            if housePrice != 0:
                if cell in houseCoor:
                    minimum = houseCoor[cell].price / \
                        houseCoor[cell].numberOfNeighbours
                    ratio = loadedInput[x][y].price / \
                        loadedInput[x][y].numberOfNeighbours
                    if minimum > ratio:
                        houseCoor[cell].price = housePrice
                        houseCoor[cell].x = x
                        houseCoor[cell].y = y
                else:
                    houseCoor[cell] = House(x, y, housePrice)
                    houseCoor[cell].numberOfNeighbours = loadedInput[x][y].numberOfNeighbours

    return houseCoor


def formatResult(result):
    out = "" + str(len(result)) + "\n"
    for i in result:
        house = i
        out += str(result[house].x) + " " + str(result[house].y) + "\n"
    return out


def readSavedDict():
    f = open(
        "/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/ksp-h-210221-04-py/mezivypocet.txt", "r")
    houseCoordinates = {}
    for i in f:
        line = list(map(int, i.split(" ")))
        # print(line)
        if not(line[0] in houseCoordinates):
            houseCoordinates[line[0]] = {}
        houseCoordinates[line[0]][line[1]] = House(
            line[0], line[1], line[2])
        houseCoordinates[line[0]][line[1]].numberOfNeighbours = line[3]
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

mapa = init()
houseCoor = readSavedDict()
# createTestMap([11, 12356], [26, 12376])
#mapa = initTest()

endTime = time.time()
print("done init in:", (endTime - startTime)*1000, "ms")

startTime = time.time()

result = main(mapa, houseCoor, 500)
# print(result)
outputContent = formatResult(result)


saveOutput(outputContent)
endTime = time.time()
print("done main in", (endTime - startTime)*1000, "ms")
