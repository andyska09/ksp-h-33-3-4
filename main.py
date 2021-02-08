import numpy
import time
from array import array


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


def initTest(start, end):
    S = end[1] + 1
    mapa = []
    print("start")
    with open("/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/01.in", "rb") as input_file:
        for y in range(end[0]+1):
            if y < start[0]:
                numpy_radek = numpy.fromfile(
                    input_file,
                    dtype="<u2",
                    count=0
                )
            else:
                numpy_radek = numpy.fromfile(
                    input_file,
                    dtype="<u2",
                    count=S
                )
                radek = array('H')
                radek.fromlist(numpy_radek.tolist())
                mapa.append(radek)
    return extractTestMap(mapa, start, end)


def extractTestMap(mapa, start, end):
    newMap = []
    x = 0
    for i in range(start[0], end[0] + 1):
        newMap.append(array('H'))
        for j in range(start[1], end[1] + 1):
            newMap[x].append(mapa[x][j])
        x += 1
    return newMap


print("start")
start = time.time()
mapa = initTest([8000, 10000], [8020, 10020])
end = time.time()
print("done init in:", (end - start)*1000, "ms")
totalValue = 0

start = time.time()
for i in range(len(mapa)):
    for j in range(len(mapa[0])):
        totalValue += mapa[i][j]
end = time.time()
print("done main in", (end - start)*1000, '\n', totalValue)
