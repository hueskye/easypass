"""Module contains methods for generating features from n-grams."""

import numpy as np


def create_coordinates(laymap, string, noshift=True):
    row = np.array([])

    for char in string:
        coors = (laymap[char][:2] if noshift else laymap[char])
        row = np.append(row, coors)

    return row
