"""Main password generator program."""

import sys

import neurolab as nl

import features
import passgen
import util


def usage_and_exit():
    print "Usage: python", sys.argv[0], "conf.net size [size [..]]"
    sys.exit(1)


def main():
    # Parse command line arguments.
    if len(sys.argv) < 3:
        usage_and_exit()

    net_conf_fname = sys.argv[1]

    scorer = passgen.Scorer(nl.load(net_conf_fname),
                            features.transform_power,
                            util.layout_mapping())

    all_chars = ''.join(util.NORMAL_LAYOUT)

    # Generate and print a password.
    for size in sys.argv[2:]:
        print size, ':',
        print passgen.generate(scorer, all_chars, int(size), 3)


if __name__ == '__main__':
    main()
