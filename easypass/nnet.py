"""Module with all neural-network related in this project."""

import neurolab as nl
import numpy as np


class NeurolabNNet(object):
    """Neurolab neural net implementation."""

    def __init__(self, *args):
        bounds, layers = args
        self.net = nl.net.netww(bounds, layers)

    def train(self, train_set, *args):
        epo, goa = args

        size = len(train_set)
        inp = train_set[:, :-1]
        tar = train_set[:, -1].reshape(size, 1)

        return self.net.train(inp, tar, epochs=epo, show=0, goal=goa)

    def simulate(self, inp):
        return self.net.sim(inp)


class NGramScorer(object):

    def __init__(self, net, feature_fun):
        self.net = net
        self.ffun = feature_fun

    def score(self, ngram):
        return self.net.simulate(self.ffun(ngram))


def test_nnet(net, test_set):
    size = len(test_set)
    out = net.simulate(test_set[:, :-1])
    tar = test_set[:, -1].reshape(size, 1)
    return np.sum(np.square(out - tar)) / size


def cross_validate(dataset):
    bounds = [[0, 3.6], [0, 15], [0, 1]] * 4

    # All various combinations of parameters.
    all_layers = [[10, 1], [20, 1], [30, 1], [40, 1], [50, 1]]
    all_epochs = [50, 100, 200, 300, 400, 500]
    all_goals = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]

    # Yay.
    np.random.shuffle(dataset)

    min_error = 10101001089
    best_params = 'prejadno'

    for layers in all_layers:
        for epochs in all_epochs:
            for goals in all_goals:
                # Now split dataset in 4 or 8 pieces.
                piece = len(dataset) / 8
                errors = []
                for part in xrange(0, 8):
                    train_set = dataset[:150]
                    test_set = dataset[150:]

                    net = NeurolabNNet(bounds, layers)
                    net.train(train_set, epochs, goals)

                    errors.append(test_nnet(net, test_set))

                    dataset = np.roll(dataset, piece)

                error = np.mean(errors)
                if error < min_error:
                    best_params = (layers, epochs, goals)

                print layers, epochs, goals, ':', error

    return best_params


def main():
    pass


if __name__ == '__main__':
    main()
