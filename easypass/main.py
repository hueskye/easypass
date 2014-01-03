"""Main password generator program."""

import sys

import features
import knn
import nnet
import passgen
import svm
import util


def usage_and_exit():
    # TODO(matija)
    sys.exit(1)
    pass


def main():
    # Parse command line arguments.
    if len(sys.argv) < 4:
        usage_and_exit()

    pass_size = int(sys.argv[1])
    reg_type = sys.argv[2]
    reg_fname = sys.argv[3]

    # Stuff we need to generate a password.
    reg = None
    if reg_type == 'nnet':
        reg = nnet.load(reg_fname)
    elif reg_type == 'svm':
        reg = svm.load(reg_fname)
    elif reg_type == 'knn':
        reg = knn.load(reg_fname)
    else:
        usage_and_exit()

    feature_fun = features.create_coor
    all_chars = ''.join(util.NORMAL_LAYOUT)
    scorer = passgen.Scorer(reg, feature_fun)

    # Generate and print a password.
    print passgen.generate(scorer, all_chars, pass_size, 4)


if __name__ == '__main__':
    main()
