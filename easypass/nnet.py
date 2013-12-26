"""Module with all neural-network related in this project."""

import csv

import neurolab as nl
import numpy as np

import util


def create_input(laymap, string):
    row = np.array([])
    for chr in string:
        row = np.append(row, laymap[chr])

    return row


def create_dataset(fname, laymap, k_param=4, num_scores=3):
    """Open CSV file, read data and create dataset ready for training."""
    with open(fname) as infile:
        reader = csv.reader(infile, delimiter='\t', quoting=csv.QUOTE_NONE)

        inp = np.array([])
        tar = np.array([])
        size = 0

        for row in reader:
            if reader.line_num == 1:
                continue

            assert len(row) == num_scores + 1
            assert len(row[0]) == k_param

            inp = np.append(inp, create_input(laymap, row[0]))
            score = np.mean([float(s) for s in row[1:]])
            tar = np.append(tar, score)

            size += 1

        assert len(inp) == size * k_param * 3
        inp = inp.reshape(size, k_param * 3)
        tar = (tar.reshape(size, 1) - 3) / 2

        return np.hstack((inp, tar))


def create_and_train(dataset, nnet_init, nnet_train):
    size = len(dataset)
    inp, tar = dataset[:, :-1], dataset[:, -1]
    tar = tar.reshape(size, 1)
    bounds, layers = nnet_init
    epo, goa = nnet_train

    net = nl.net.newff(bounds, layers)
    err = net.train(inp, tar, epochs=epo, show=0, goal=goa)

    return net, err


def simulate(net, laymap, string):
    return net.sim([create_input(laymap, string)])


def test_nnet(net, test_set):
    size = len(test_set)
    out = net.sim(test_set[:, :-1])
    tar = test_set[:, -1].reshape(size, 1)
    # Normalized the way neurolab does it!
    return np.sum(np.square(out - tar)) / 2


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

                    net, err = create_and_train(train_set,
                                                (bounds, layers),
                                                (epochs, goals))

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
