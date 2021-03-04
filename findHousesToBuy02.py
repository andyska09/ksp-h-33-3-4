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

    def updateCoverage(self, startRow, endRow, startCollumn, endCollumn, prefixes):
        countToRemove = 0

        for row in range(startRow, endRow):
            countOnEnd = prefixes[row][endCollumn]
            countOnStart = prefixes[row][startCollumn]
            if startCollumn < 0:
                countOnStart = 0
            countToRemove += countOnEnd - \
                countOnStart
        self.numberOfNeighbours -= countToRemove


def findHousesToBuy(houseCoor, mapa, k):
    print("start findHouseToBuy")
    startTime = time.time()
    prefixes = calcPrefixes(mapa)
    endTime = time.time()
    print("finished calcPrefixes:", (endTime - startTime)*1000, "ms")
    housesToBuy = []

    print("start search")
    for i in range(10000):
        print(i)
        maxCoor = findMax(houseCoor)
        housesToBuy.append(maxCoor)
        if i % 30 == 0:
            saveOutput(formatResult(housesToBuy))
        if maxCoor[0] == -1:
            print("ended before 10,000")
            break
        startTime = time.time()
        prefixes = readjustCoverege(houseCoor, prefixes, k, maxCoor)
        endTime = time.time()
        print("readjusted coverage:", (endTime - startTime)*1000, "ms")
    return housesToBuy


def readjustCoverege(houseCoor, prefixes, k, maxCoor):
    x = maxCoor[0]
    y = maxCoor[1]
    numberCollumns = len(prefixes[0])
    numberRows = len(prefixes)
    startX = max(0, x - 2*k)
    endX = min(len(houseCoor), x + 2*k + 1)
    startY = max(0, y - 2*k)
    endY = y + 2*k
    for row in range(startX, endX):
        for j in houseCoor[row]:
            if j >= startY:
                if j <= endY:
                    if row < x:
                        startRow = max(0, x - k)
                        endRow = min(numberRows, row + k + 1)
                    elif row == x:
                        startRow = max(0, x - k)
                        endRow = min(numberRows, x + k + 1)
                    else:
                        startRow = max(0, row - k)
                        endRow = min(numberRows, x + k + 1)
                    if j < y:
                        startCollumn = y - k - 1
                        endCollumn = min(numberCollumns - 1, j + k)
                    elif j == y:
                        startCollumn = y - k - 1
                        endCollumn = min(numberCollumns - 1, y + k)
                    else:
                        startCollumn = j - k - 1
                        endCollumn = min(numberCollumns - 1, y + k)
                    houseCoor[row][j].updateCoverage(
                        startRow, endRow, startCollumn, endCollumn, prefixes)
                else:
                    break
    startX = max(0, x - k)
    endX = min(numberRows, x + k + 1)

    startY = y - k - 1
    endY = min(numberCollumns - 1, y + k)
    for row in range(startX, endX):
        countOnEnd = prefixes[row][endY]
        if 0 > startY:
            countOnStart = 0
        else:
            countOnStart = prefixes[row][startY]
        difference = countOnEnd - countOnStart
        for j in range(max(0, startY), numberCollumns):
            if j < endY:
                prefixes[row][j] = countOnStart
            else:
                prefixes[row][j] -= difference
    return prefixes


def findMax(houseCoor):
    minimum = -1
    maxCoor = [-1, -1]
    startTime = time.time()
    for i in houseCoor:
        for j in houseCoor[i]:
            if houseCoor[i][j].numberOfNeighbours != 0:

                if minimum == -1:
                    minimum = houseCoor[i][j].price
                    maxCoor = [i, j]
                elif houseCoor[i][j].price <= minimum:
                    if houseCoor[i][j].numberOfNeighbours > houseCoor[maxCoor[0]][maxCoor[1]].numberOfNeighbours:
                        minimum = houseCoor[i][j].price
                        maxCoor = [i, j]
    endTime = time.time()
    print("found Max:", (endTime - startTime)*1000, "ms", maxCoor)
    return maxCoor


def calcPrefixes(mapa):
    prefixes = []
    numberRows = len(mapa)
    numberCollumns = len(mapa[0])
    for x in range(numberRows):
        prefixes.append([])
        for y in range(numberCollumns):
            if y == 0:
                lastPrefix = 0
            else:
                lastPrefix = prefixes[x][y - 1]
            prefixes[x].append(lastPrefix)
            if mapa[x][y] != 0:
                prefixes[x][y] += 1
    return prefixes


def readSavedDict():
    f = open("/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/ksp-h-210221-04-py/mezivypocet.txt", "r")
    houseCoor = {}
    for i in f:
        line = list(map(int, i.split(" ")))
        # print(line)
        if not(line[0] in houseCoor):
            houseCoor[line[0]] = {}
        houseCoor[line[0]][line[1]] = House(
            line[0], line[1], line[2])
        houseCoor[line[0]][line[1]].numberOfNeighbours = line[3]
    return houseCoor


def saveOutput(outputContent):
    savePath = "/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/ksp-h-210221-04-py/outputs"
    name = datetime.now().strftime("%y%m%d-%H-%M-%S")
    completeName = os.path.join(savePath, name+"-out.txt")
    f = open(completeName, "w")
    f.write(outputContent)
    f.close()


def formatResult(result):
    out = "" + str(len(result)) + "\n"
    for i in range(len(result)):
        house = result[i]
        out += str(house[0]) + " " + str(house[1]) + "\n"
    return out


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


print("start")
startTime = time.time()

houseCoor = readSavedDict()
mapa = init()
#mapa = initTest()

endTime = time.time()
print("done init in:", (endTime - startTime)*1000, "ms")

startTime = time.time()

result = findHousesToBuy(houseCoor, mapa, 500)
print(result)
outputContent = formatResult(result)

saveOutput(outputContent)
endTime = time.time()
print("done main in", (endTime - startTime)*1000, "ms")
