# python file to run game of life simulation

from PeriodicLattice import PeriodicLattice
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


def getInputParams():
    dimensions = int(sys.argv[1])
    initState = sys.argv[2]
    maxSweeps = int(sys.argv[3])

    return dimensions, initState, maxSweeps

def updateLattice(lattice):
    print("update lattice has been called")
    returnLat = PeriodicLattice(lattice.size(), 8)

    for (x,y), state in np.ndenumerate(lattice.getLattice()):
        # apply update rules here
        NNs = lattice.getNearestNeighbours((x,y))
        NNTotal = sum([lattice[NN] for NN in NNs])

        if (NNTotal < 2 or NNTotal > 3):
            returnLat[(x,y)] = 0
        elif (NNTotal == 3):
            returnLat[(x,y)] = 1
        elif (NNTotal == 2 and state == 1):
            returnLat[(x,y)] = 1

    return returnLat


def main():

    dimensions, initState, maxSweeps = getInputParams()

    lattice = PeriodicLattice(dimensions, 8, initState)

    fig = plt.figure()
    ax = fig.add_subplot(222)
    im = ax.imshow(lattice.getLattice())
    plt.show(block=False)

    for sweep in range(maxSweeps):
        print(sweep)
        lattice = updateLattice(lattice)
        time.sleep(0.04)

        # redraw plot
        im.set_array(lattice.getLattice())
        fig.canvas.draw()

main()
