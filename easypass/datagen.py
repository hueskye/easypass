"""Module for generating n-gram input data."""

import numpy as np

import util


def _create_trans_probs(layout_map, all_chars, dist_coef):
    """Create transitive probability matrix between characters."""
    trans_probs = dict()

    for src_chr in all_chars:
        probs = np.empty(len(all_chars))

        for cix, dst_chr in enumerate(all_chars):
            coor1, coor2 = layout_map[src_chr], layout_map[dst_chr]
            if src_chr != dst_chr:
                probs[cix] = np.linalg.norm(coor1 - coor2)
            else:
                probs[cix] = 10000000000000000

        probs = np.exp(-probs / dist_coef)

        trans_probs[src_chr] = util.DiscreteRandom(all_chars, probs)

    return trans_probs


def _create_ngram(char, trans_probs, ngram_size):
    ngram = str(char)
    for idx in xrange(ngram_size - 1):
        drv = trans_probs[ngram[-1]]
        ngram += drv.random()

    return ngram


def generate_dist(layout_map, all_chars, ngram_size=4, dist_coef=10):
    """Generate input data using stochastic distance based method."""
    trans_probs = _create_trans_probs(layout_map, all_chars, dist_coef)

    dataset = []
    for char in all_chars:
        left_part = _create_ngram(char, trans_probs, ngram_size)
        right_part = _create_ngram(char, trans_probs, ngram_size)
        example = left_part[::-1] + right_part[1:]

        assert len(left_part) == ngram_size and len(right_part) == ngram_size
        assert len(example) == 2 * ngram_size - 1

        start = np.random.randint(ngram_size)
        dataset.append(example[start:start + ngram_size])

    return dataset


def main():
    pass


if __name__ == '__main__':
    main()
