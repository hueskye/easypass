"""Module with various project utilities."""

import numpy as np


NORMAL_LAYOUT = ['1234567890-=',
                 'qwertyuiop[]',
                 'asdfghjkl;\'',
                 'zxcvbnm,./']

SHIFT_LAYOUT = ['!@#$%^&*()_+',
                'QWERTYUIOP{}',
                'ASDFGHJKL:"',
                'ZXCVBNM<>?']


def layout_mapping(spacing=1.2, row_offsets=None):
    """Return full mapping from char to coordinates (row, col, shift)."""
    layout_map = dict()

    if not row_offsets:
        row_offsets = [0, 0.6, 1, 1.6]

    for row_num in xrange(4):
        row_coor, col_coor = row_num * spacing, row_offsets[row_num]
        nrow, srow = NORMAL_LAYOUT[row_num], SHIFT_LAYOUT[row_num]

        assert len(nrow) == len(srow)
        for col_num in xrange(len(NORMAL_LAYOUT[row_num])):
            layout_map[nrow[col_num]] = np.array([row_coor, col_coor, 0])
            layout_map[srow[col_num]] = np.array([row_coor, col_coor, 1])
            col_coor += spacing

    return layout_map


class DiscreteRandom(object):
    """Discrete random generator."""

    def __init__(self, values, probabilities):
        self.probs = np.array(probabilities)
        self.probs = np.add.accumulate(self.probs)
        self.vals = np.array(values)

    def random(self):
        """Return single random value according to it's probability."""
        idx = np.digitize(np.random.random_sample(1), self.probs)
        return self.vals[idx][0]


def main():
    """Do nothing."""
    pass


if __name__ == '__main__':
    main()
