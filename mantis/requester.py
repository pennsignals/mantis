import sys
import time

from urllib.request import Request

from . import CRLF
from .command import HTTPCommand, RequestInvoker
from .handler import DefaultRequestHandler
from .publisher import Publisher


class Requester:

    DEFAULT_TIMEOUT_INTERVAL = 10

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
        self.publisher = Publisher()

    def request(self, duration=DEFAULT_TIMEOUT_INTERVAL):
        start = time.time()
        arguments = self.arguments
        invoker = RequestInvoker()
        invoker.register('onRequest', DefaultRequestHandler())
        while True:
            try:
                command = HTTPCommand(Request(arguments.address, headers=arguments.header))
                invoker('onRequest', command)
                self.publisher(message=command.body)
                time.sleep(duration)
            except KeyboardInterrupt:
                elapsed = time.time() - start
                sys.exit('{newline}{elapsed}'.format(newline=CRLF, elapsed=elapsed))
