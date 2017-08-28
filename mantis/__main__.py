import argparse

from base64 import b64encode

from . import (
    __version__,
    DEFAULT_CHARACTER_ENCODING,
    Requester,
)


def initialize(arguments):
    requester = Requester(__name__, arguments)
    requester.request(duration=arguments.duration)


def authenticate(user, encoding=DEFAULT_CHARACTER_ENCODING):
    return 'Basic {user}'.format(user=b64encode(user.encode(encoding)).decode(encoding))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    initializer = subparsers.add_parser('up')
    initializer.add_argument('-X', '--request', type=str, default='GET')
    initializer.add_argument('-H', '--header', metavar='LINE', action='append', type=lambda headers: headers.split(':'), help='Pass custom header LINE to server (H)')  # noqa: E501
    initializer.add_argument('-u', '--user', metavar='USER[:PASSWORD]', type=authenticate, help='Server user and password')  # noqa: E501
    initializer.add_argument('--remote', type=str)
    initializer.add_argument('--duration', type=int, default=Requester.DEFAULT_TIMEOUT_INTERVAL)
    initializer.add_argument('address', type=str)
    initializer.set_defaults(func=initialize)

    parser.add_argument('--version', action='version', version=__version__)

    arguments = parser.parse_args()

    if arguments.header is None:
        arguments.header = {}
    arguments.header = dict(arguments.header)
    if arguments.user:
        arguments.header['Authorization'] = arguments.user

    arguments.func(arguments)


if __name__ == '__main__':
    main()
