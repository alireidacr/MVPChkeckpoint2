# python script to implement SIRS model

from PeriodicLattice import PeriodicLattice
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import random as rnd

def getInputParams():
    dimensions = int(sys.argv[1])
    prob1 = float(sys.argv[2])
    prob2 = float(sys.argv[3])
    prob3 = float(sys.argv[4])
    probs = (prob1, prob2, prob3)
    initState = sys.argv[5]

    if (len(sys.argv) == 7):
        immuneNum = int(sys.argv[6])
    else:
        immuneSites = 0

    return dimensions, probs, initState, immuneNum

def generateInitState(dimensions, initState, immuneNum):
    grid = np.zeros((dimensions, dimensions))

    if (initState == "random"):
        options = [0, 1, 2]
        immuneCounter = 0
        immuneSites = []

        for pos, state in np.ndenumerate(grid):
            grid[pos] = rnd.choice(options)

        for immuneCounter in range(immuneNum):
            randx = rnd.randint(0, dimensions -1)
            randy = rnd.randint(0, dimensions -1)
            randPos = (randx, randy)

            if (not randPos in immuneSites):
                immuneSites.append(randPos)

    return grid, immuneSites

def updateLattice(lattice, probs, immuneSites):
    latticeNum = lattice.size()**2

    for i in range(latticeNum):
        pos = (rnd.randint(0, 49), rnd.randint(0, 49))
        NNs = lattice.getNearestNeighbours(pos)
        NNStates = [lattice[NN] for NN in NNs]

        if (lattice[pos] == 0 and 1 in NNStates):
            # site is susceptible and has at least one infected neighbour
            if (rnd.random() < probs[0]):
                lattice[pos] = 1

        elif (lattice[pos] == 1):
            # site is infected
            if (rnd.random() < probs[1]):
                # site becomes recovered with certain probability
                lattice[pos] = 2

        elif (lattice[pos] == 2):
            # site is recovered
            if (rnd.random() < probs[2] and not pos in immuneSites):
                # site becomes susceptible again with certain probability
                lattice[pos] = 0

    return lattice

def getInfectedNum(lattice):
    infectedCounter = 0;
    for pos, state in np.ndenumerate(lattice.getLattice()):
        if (state == 1):
            infectedCounter += 1

    return infectedCounter

def recordMeanInfected(infectedNums, probs, dimensions):
    meanInfFile = open("meanInfected.txt", "a+")
    meanInfected = (sum(infectedNums)/len(infectedNums))/dimensions**2
    meanInfFile.write(str(probs[0]) + " " + str(probs[2]) + " " + str(meanInfected) + "\n")
    meanInfFile.close()

def recordVarianceInfected(infectedNums, probs, dimensions):
    VarInfFile = open("VarInfected.txt", "a+")
    squares = [num**2 for num in infectedNums]
    meanSquares = sum(squares)/len(squares)
    meanInf = sum(infectedNums)/len(infectedNums)
    varInf = ((meanSquares - meanInf**2)/len(infectedNums))/dimensions**2

    VarInfFile.write(str(probs[0]) + " " + str(probs[2]) + " " + str(varInf) + "\n")
    VarInfFile.close()

def recordMeanInfImmune(infectedNums, immuneFrac, dimensions):
    meanInfFile = open("meanImmune.txt", "a+")
    meanInfected = (sum(infectedNums)/len(infectedNums))/dimensions**2
    meanInfFile.write(str(immuneFrac) + " " + str(meanInfected) + "\n")
    meanInfFile.close()

def reDraw(lattice, im, fig):
    im.set_array(lattice.getLattice())
    fig.canvas.draw()

    return im

def dummy(lattice, im, fig):
    return im

def main():

    dimensions, probs, initState, immuneNum = getInputParams()

    initGrid, immuneSites = generateInitState(dimensions, initState, immuneNum)
    lattice = PeriodicLattice(dimensions, 4, initGrid)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(lattice.getLattice(), cmap='CMRmap')
    cbar = plt.colorbar(im, ticks=[0, 1, 2])
    cbar.ax.set_yticklabels(['Susceptible', 'Infected', 'Recovered'])

    if (probs == (0, 0, 0)):
        p1Vals = np.linspace(0.25, 0.4, 30)
        p2Val = 0.5
        p3Vals = np.linspace(0.5, 0.5, 1)

        visFunc = dummy

    else:
        p1Vals = [probs[0]]
        p2Val = probs[1]
        p3Vals = [probs[2]]

        plt.show(block=False)

        visFunc = reDraw


    for p1 in p1Vals:
        for p3 in p3Vals:
            probs = (p1, p2Val, p3)
            infectedNums = []
            initGrid, immuneSites = generateInitState(dimensions, initState, immuneNum)
            lattice.setLattice(initGrid) # reset lattice to initial state

            for sweep in range(10100):
                if (sweep > 100 and sweep % 10 == 0):
                    lattice = updateLattice(lattice, probs, immuneSites)
                    infectedNums.append(getInfectedNum(lattice))
                    visFunc(lattice, im, fig)

            recordMeanInfected(infectedNums, probs, lattice.size())
            recordVarianceInfected(infectedNums, probs, lattice.size())
            #recordMeanInfImmune(infectedNums, immuneFrac, lattice.size())

main()
