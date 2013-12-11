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
        tar = (tar.reshape(size, 1) - 1) / 4

        return inp, tar


def create_and_train(dataset, nnet_init, nnet_train):
    inp, tar = dataset
    bounds, layers = nnet_init
    epo, sho, goa = nnet_train

    net = nl.net.newff(bounds, layers)
    err = net.train(inp, tar, epochs=epo, show=sho, goal=goa)

    return net, err


def simulate(net, laymap, string):
    return net.sim([create_input(laymap, string)])


def main():
    pass


if __name__ == '__main__':
    main()
