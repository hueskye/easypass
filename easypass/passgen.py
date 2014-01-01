"""Module for generating passwords."""

import numpy as np

import util


class Scorer(object):
    """Simple class to group feature creation and scoring for n-grams."""

    def __init__(self, ml_alg, feature_fun):
        self.ml = ml_alg
        self.ff = feature_fun

    def score(self, ngram):
        """Score this n-gram string."""
        return self.ml.simulate(self.ff(ngram))


def _random_char(all_chars, unwanted_chars):
    """Return random char from 'all_chars' not in 'unwanted_chars'."""
    while True:
        newchar = all_chars[np.random.randint(len(all_chars))]
        if newchar not in unwanted_chars:
            return newchar


def _random_ngram(all_chars, ngram_size):
    """Return random n-gram with non-repetitive chars."""
    ngram = ['`']

    for cix in xrange(ngram_size):
        ngram.append(_random_char(all_chars, [ngram[-1]]))

    return ''.join(ngram[1:])


def generate(scorer, all_chars, pass_size, ngram_size):
    """Generate a high-quality password of desired size and a set of chars."""
    # Algorithm parameters.
    init_thresh = 0.5
    next_thresh = 0.5
    num_letter_seeds = 10

    # Initialize with a good n-gram.
    while True:
        password = _random_ngram(all_chars, ngram_size)
        if scorer.score(password) >= init_thresh:
            break

    # Continue building up to desired size.
    while len(password) < pass_size:
        # Seed random characters until there are enough good ones. Quality is
        # determined by the score of the new n-gram and is used to calculate
        # new probability of picking that character.
        chars = [password[-1]]
        probs = [0]
        goods = 0
        while goods < num_letter_seeds and len(chars) < len(all_chars):
            newchar = _random_char(all_chars, chars)
            newscore = scorer.score(password[1 - ngram_size:] + newchar)

            chars.append(newchar)
            if newscore < next_thresh:
                probs.append(0)
            else:
                probs.append(newscore + 1)
                goods += 1

        # Take a random char if there enough good ones seeded, otherwise
        # do quasi-backtracking by removing a character or starting again if
        # the current password is to short.
        if goods > num_letter_seeds / 2:
            drv = util.DiscreteRandom(chars, probs)
            password += drv.random()
        elif len(password) > ngram_size:
            password = password[:-1]
        else:
            password = generate(scorer, all_chars, pass_size, ngram_size)

    return password


def main():
    pass


if __name__ == '__main__':
    main()
