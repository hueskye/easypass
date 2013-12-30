"""Module contains methods for generating features from n-grams."""

import numpy as np


def create_coordinates(laymap, string, noshift=True):
    """Basic coordinate based mapping from n-gram to features."""
    row = np.array([])

    for char in string:
        coors = (laymap[char][:2] if noshift else laymap[char])
        row = np.append(row, coors)

    return row


def normalize(dataset):
    """Normalize all columns of dataset to range [-1, 1]."""
    for cix in xrange(dataset.shape[1]):
        minval, maxval = np.min(dataset[:, cix]), np.max(dataset[:, cix])
        dataset[:, cix] -= (maxval + minval) / 2
        dataset[:, cix] /= (maxval - minval) / 2


def main():
    pass


if __name__ == '__main__':
    main()
