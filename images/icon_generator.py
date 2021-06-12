#!/usr/bin/env python3

import sys
from PIL import Image
from PIL import ImageOps


def usage():
    print('usage: ./icon_generator.py <src_image>')


def main(filename):
    icon_sizes = (16, 32, 48, 128)
    src_image = Image.open(filename, 'r')
    pure_filename = filename.split('.')[-2].split('\\')[-1]

    for size in icon_sizes:
        icon = src_image.resize((size, size), Image.LANCZOS)
        icon.save('./icons/{}_{}.png'.format(pure_filename, size))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    filename = sys.argv[1]
    main(filename)
