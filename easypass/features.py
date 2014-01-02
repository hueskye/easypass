"""Module contains methods for generating features from n-grams."""

import numpy as np


def create_coor(laymap, string, noshift=True):
    """Basic coordinate based mapping from n-gram to features."""
    row = np.array([])

    for char in string:
        coors = (laymap[char][:2] if noshift else laymap[char])
        row = np.append(row, coors)

    return row


def normalize(dataset, minmax):
    """Normalize all columns of dataset to range [-1, 1]."""
    for cix in xrange(dataset.shape[1]):
        minval, maxval = minmax[cix]
        dataset[:, cix] -= (maxval + minval) / 2
        dataset[:, cix] /= (maxval - minval) / 2


def extend_power(dataset, extensions):
    """Extend dataset with feature powers."""
    for cix, power in extensions:
        newcol = np.vstack(np.power(dataset[:, cix], power))
        dataset = np.hstack((dataset, newcol))


def main():
    pass


if __name__ == '__main__':
    main()
