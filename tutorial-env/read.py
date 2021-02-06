import sys
import numpy
from array import array


def init():
    S = 16384
    mapa = []
    print("start")
    for y in range(S):
        # Musíme dát pozor na endianitu (data jsou
        # little-endian) a tak načtení svěříme numpy
        numpy_radek = numpy.fromfile(
            "/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/01.in",
            dtype="<u2",  # unsigned 2bajtová čísla
            count=S       # v little-endian(<)
        )
        # Pro rychlejší přístup k prvkům převedeme
        # na interní Pythoní pole
        radek = array('H')  # minimálně 2b číslo
        radek.fromlist(numpy_radek.tolist())
        mapa.append(radek)
    return mapa


def initTest(start, end):
    S = end[1] + 1
    mapa = []
    print("start")
    for y in range(end[0]+1):
        # Musíme dát pozor na endianitu (data jsou
        # little-endian) a tak načtení svěříme numpy
        numpy_radek = numpy.fromfile(
            "/Users/ondrej/workspace/code/ksp-h-20/ksp-h-210221/01.in",
            dtype="<u2",  # unsigned 2bajtová čísla
            count=S       # v little-endian(<)
        )
        # Pro rychlejší přístup k prvkům převedeme
        # na interní Pythoní pole
        radek = array('H')  # minimálně 2b číslo
        radek.fromlist(numpy_radek.tolist())
        mapa.append(radek)
    extractTestMap(mapa, start, end)
    return mapa


def extractTestMap(mapa, start, end):
    newMap = []
    for i in range(start[0], end[0] + 1):
        newMap.append(array('H'))
        for j in range(start[1], end[1] + 1):
            newMap[i].append(mapa[i][j])
    return newMap


mapa = initTest([0, 0], [1, 10])

count = 0
totalPrice = 0
print(mapa)

for i in range(len(mapa)):
    for j in range(len(mapa[0])):
        if mapa[i][j] != 0:
            count += 1
            totalPrice += mapa[i][j]

print(count)
print(totalPrice)
