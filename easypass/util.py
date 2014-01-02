"""Module with various project utilities."""

import csv

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
        self.probs /= np.add.reduce(self.probs)
        self.probs = np.add.accumulate(self.probs)
        self.vals = values

    def random(self):
        """Return single random value according to it's probability."""
        idx = np.digitize(np.random.random_sample(1), self.probs)[0]
        return self.vals[idx]


def read_data(fname, ngram_size=4):
    """Open CSV file, read data and create dataset ready for training."""
    with open(fname) as infile:
        reader = csv.reader(infile, delimiter='\t', quoting=csv.QUOTE_NONE)

        data = np.array([])
        size = 0

        for row in reader:
            assert len(row[0]) == ngram_size

            for elem in row:
                data = np.append(data, elem)

            size += 1

        return data.reshape(size, len(data) / size)


def main():
    pass


if __name__ == '__main__':
    main()
