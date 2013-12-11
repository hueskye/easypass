"""Module with various project utilities."""

import numpy as np


NORMAL_LAYOUT = ['1234567890-=',
                 'qwertyuiop[]\\',
                 'asdfghjkl;\'',
                 'zxcvbnm,./']

SHIFT_LAYOUT = ['!@#$%^&*()_+',
                 'QWERTYUIOP{}|',
                 'ASDFGHJKL:"',
                 'ZXCVBNM<>?']


class DiscreteRandom(object):
    """Discrete random generator."""

    def __init__(self, values, probabilities):
        self.probs = np.array(probabilities)
        self.vals = values
        self.probs = np.add.accumulate(self.probs)

    def random(self):
        """Return single random value according to it's probability."""
        return self.vals[np.digitize(np.random.random_sample(1), self.probs)][0]


def layout_mapping():
    """Return full mapping from char to coordinates (row, col, shift)."""
    layout_map = dict()
    row_offsets = [0, 0.6, 1, 1.6]
    spacing = 1.2

    for row_num in xrange(4):
        row_coor, col_coor = row_num * spacing, row_offsets[row_num]
        nrow, srow = NORMAL_LAYOUT[row_num], SHIFT_LAYOUT[row_num]

        assert len(nrow) == len(srow)
        for col_num in xrange(len(NORMAL_LAYOUT[row_num])):
            layout_map[nrow[col_num]] = (row_coor, col_coor, 0)
            layout_map[srow[col_num]] = (row_coor, col_coor, 1)
            col_coor += spacing

    return layout_map


def generate_dataset(layout_map, all_chars, dist_coef=10, shift_coef=5):
    """Generate data given a layout map and a set of characters."""
    # Calculate transition probabilities for each character.
    trans_probs = dict()
    for src_chr in all_chars:
        probs = np.empty(len(all_chars))
        for cix, dst_chr in enumerate(all_chars):
            coor1, coor2 = layout_map[src_chr], layout_map[dst_chr]
            probs[cix] =  np.sqrt(np.square(coor1[0] - coor2[0]) +
                                  np.square(coor1[1] - coor2[1]) +
                                  abs(coor1[2] - coor2[2]) * shift_coef)

        probs = np.exp(-probs / dist_coef)
        probs /= np.add.reduce(probs)
        trans_probs[src_chr] = DiscreteRandom(probs, all_chars)

    # Generate dataset.
    dataset = []
    for char in all_chars:
        example1, example2 = str(char), str(char)
        for idx in xrange(3):
            drv = trans_probs[example1[-1]]
            example1 += drv.random()

            drv = trans_probs[example2[-1]]
            example2 += drv.random()

        example = example1[::-1] + example2[1:]
        start = np.random.randint(4)
        dataset.append(example[start:start+4])

    return dataset

def main():
    pass


if __name__ == '__main__':
    main()
