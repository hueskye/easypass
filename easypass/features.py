"""Module contains methods for generating features from n-grams."""

import numpy as np

import util


def _dist(coor1, coor2, noshift=True):
    """Return distance between coordinates."""
    last = (2 if noshift else 3)
    return np.linalg.norm(coor1[:last] - coor2[:last])


def _max_coors(laymap):
    """Return maximal X and Y coordinates in this layout."""
    max_x, max_y = 0.0, 0.0
    for key, val in laymap.iteritems():
        max_x = max(max_x, val[0])
        max_y = max(max_y, val[1])

    return (max_x, max_y)


def _max_dist(laymap):
    """Return maximal distance between two chars in this layout."""
    max_d = 0.0
    for key, val in laymap.iteritems():
        for key2, val2 in laymap.iteritems():
            dist = _dist(val, val2)
            max_d = max(max_d, dist)

    return max_d


def _normalized_coor(coor, max_coors, noshift=True):
    """Calculate normalized coordinates."""
    max_x, max_y = max_coors

    coor_x = 2.0 * coor[0] / max_x - 1
    coor_y = 2.0 * coor[1] / max_y - 1
    coor_s = 2.0 * coor[2] - 1

    return (coor_x, coor_y) if noshift else (coor_x, coor_y, coor_s)


def _normalized_distangle(coor1, coor2, minmax_dist):
    """Calculate normalized distance and angle."""
    min_dist, max_dist = minmax_dist

    diff = coor1[:2] - coor2[:2]
    dist = 2.0 * (np.linalg.norm(diff) - min_dist) / (max_dist - min_dist) - 1
    angle = np.angle(complex(diff[1], diff[0]), deg=True) / 180.0

    return (dist, angle)


def transform_coords(laymap, string, noshift=True):
    """Map string to normalized layout coordinates."""
    max_coors = _max_coors(laymap)

    # Transform every character in the string.
    row = np.array([])
    for char in string:
        norm_coor = _normalized_coor(laymap[char], max_coors, noshift)
        row = np.append(row, norm_coor)

    return row


def transform_distangles(laymap, string):
    """Map string according to normalized dists and angles between chars."""
    row = np.array([])

    minmax_d = (0, _max_dist(laymap))
    for lix, ltr in enumerate(string):
        coor1, coor2 = laymap[ltr], laymap[string[lix - 1]]
        row = np.append(row, _normalized_distangle(coor1, coor2, minmax_d))

    return row


def transform_handwise(laymap, string):
    """Map string according to normalized dists and angles from hands."""
    spacing = laymap['a'][0] - laymap['q'][0]
    left_hand = laymap['x'] + np.array([spacing, 0, 0])
    right_hand = laymap[','] + np.array([spacing, 0, 0])

    # Calculate min and max distances for normalization.
    max_dist_l, max_dist_r = 0, 0
    for key, val in laymap.iteritems():
        max_dist_l = max(max_dist_l, _dist(val, left_hand))
        max_dist_r = max(max_dist_r, _dist(val, right_hand))

    minmax_l = (spacing, max_dist_l)
    minmax_r = (spacing, max_dist_r)

    # Transform string.
    row = np.array([])
    for char in string:
        left_da = _normalized_distangle(laymap[char], left_hand, minmax_l)
        row = np.append(row, left_da)

        right_da = _normalized_distangle(laymap[char], right_hand, minmax_r)
        row = np.append(row, right_da)

    return row


def transform_all(laymap, string, noshift=True):
    """Map string according to all three transformations."""
    row1 = transform_coords(laymap, string, noshift)
    row2 = transform_distangles(laymap, string)
    row3 = transform_handwise(laymap, string)

    return np.hstack((row1, row2, row3))


def extend_power(dataset, extensions):
    """Extend dataset with feature powers."""
    for cix, power in extensions:
        newcol = np.vstack(np.power(dataset[:, cix], power))
        dataset = np.hstack((dataset, newcol))

    return dataset


def main():
    pass


if __name__ == '__main__':
    main()
