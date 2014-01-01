"""Main password generator program."""

import sys

import features
import nnet
import passgen
import util


def usage():
    # TODO(matija)
    pass


def main():
    # Parse command line arguments.
    pass_size = int(sys.argv[1])
    reg_type = sys.argv[2]
    reg_fname = sys.argv[3]

    # Stuff we need to generate a password.
    reg = None
    if reg_type == 'nnet':
        reg = nnet.load(reg_fname)
    elif reg_type == 'svm':
        pass
    elif reg_type == 'knn':
        pass
    else:
        usage()
        sys.exit(1)

    feature_fun = features.create_coor
    all_chars = ''.join(util.NORMAL_LAYOUT)
    scorer = passgen.Scorer(reg, feature_fun)

    # Generate and print a password.
    print passgen.generate(scorer, all_chars, pass_size, 4)


if __name__ == '__main__':
    main()
