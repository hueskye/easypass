"""Module with various project utilities."""


def layout():
    """Return two arrays representing normal and shift keyboard layout."""
    normal_layout = ['1234567890-=',
                     'qwertyuiop[]\\',
                     'asdfghjkl;\'',
                     'zxcvbnm,./']

    shift_layout = ['!@#$%^&*()_+',
                    'QWERTYUIOP{}|',
                    'ASDFGHJKL:"',
                    'ZXCVBNM<>?']

    return normal_layout, shift_layout


def layout_mapping():
    """Return full mapping from char to coordinates (row, col, shift)."""
    normal_layout, shift_layout = layout()
    layout_map = dict()
    row_offsets = [0, 0.6, 1, 1.6]
    spacing = 1.2

    for row_num in xrange(4):
        row_coor, col_coor = row_num * spacing, row_offsets[row_num]
        nrow, srow = normal_layout[row_num], shift_layout[row_num]

        assert len(nrow) == len(srow)
        for col_num in xrange(len(normal_layout[row_num])):
            layout_map[nrow[col_num]] = (row_coor, col_coor, 0)
            layout_map[srow[col_num]] = (row_coor, col_coor, 1)
            col_coor += spacing

    return layout_map


def generate_dataset():

    return chars
