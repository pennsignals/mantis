import argparse
import time

from mantis import __version__


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=int, default=1)
    parser.add_argument('--version', action='version', version=__version__)
    arguments = parser.parse_args()

    while True:
        print('Hello, World')
        time.sleep(arguments.duration)


if __name__ == '__main__':
    main()
