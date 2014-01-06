"""Module with all neural-network related in this project."""

import neurolab as nl
import numpy as np


def train(bounds, layers, epo, goa, train_set):
    """Train neural network using given parameters."""
    net = nl.net.newff(bounds, layers)
    net.trainf = nl.train.train_bfgs
    net.errorf = nl.error.MSE()

    inp = train_set[:, :-1]
    tar = train_set[:, -1].reshape(len(train_set), 1)

    print net.train(inp, tar, epochs=epo, show=0, goal=goa)[-1]
    return net


def test(net, test_set):
    """Calculate MSE for this network on the given test set."""
    size = len(test_set)
    out = net.sim(test_set[:, :-1])
    tar = test_set[:, -1].reshape(size, 1)
    return np.sum(np.square(out - tar)) / size


def cross_validate(dataset):
    """Find optimal neural network parameters."""
    num_cols = dataset.shape[1] - 1
    bounds = [[-1, 1]] * num_cols

    # All various combinations of parameters.
    all_layers = [[10, 1], [20, 1], [30, 1]]
    all_epochs = [200, 300, 400]
    all_goals = [0.001, 0.005, 0.01, 0.1, 0.5]
    # Cross validation parameters.
    num_folds = 4
    test_size = len(dataset) / num_folds
    # Solution info.
    min_error = 10101001089
    best_params = 'prejadno'

    for layers in all_layers:
        for epochs in all_epochs:
            for goal in all_goals:
                errors = []
                for part in xrange(0, num_folds):
                    train_set = dataset[test_size:]
                    test_set = dataset[:test_size]

                    net = train(bounds, layers, epochs, goal, train_set)
                    errors.append(test(net, test_set))

                    dataset = np.roll(dataset, test_size)

                error = np.mean(errors)
                if error < min_error:
                    best_params = (layers, epochs, goal)

                print layers, epochs, goal, ':', error

    return best_params


def main():
    pass


if __name__ == '__main__':
    main()
