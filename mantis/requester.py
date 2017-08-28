import sys
import time

from urllib.parse import urlparse
from urllib.request import Request

from . import CRLF, DEFAULT_CHARACTER_ENCODING
from .command import HTTPCommand, RequestInvoker
from .handler import DefaultRequestHandler
from .loader import DefaultPackageLoader
from .publisher import Publisher


class Requester:

    DEFAULT_TIMEOUT_INTERVAL = 10

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
        self.publisher = Publisher()
        self.loader = DefaultPackageLoader()

    def request(self, duration=DEFAULT_TIMEOUT_INTERVAL):
        start = time.time()
        arguments = self.arguments
        identifier = urlparse(arguments.address)
        path = self.loader.specification.paths[identifier.path]
        operation = getattr(path, arguments.request.lower())
        # TODO: Separate OpenAPI bootstrapping functionality
        handler = self.loader.module.__dict__.get(
            operation.__dict__.get('x_request_handler', DefaultRequestHandler)
        )
        cls = type(handler.__class__.__name__, (handler, DefaultRequestHandler,), {})
        invoker = RequestInvoker()
        invoker.register('onRequest', cls())
        while True:
            try:
                command = HTTPCommand(Request(arguments.address, headers=arguments.header))
                invoker('onRequest', command)
                self.publisher(message=command.response.body.encode(DEFAULT_CHARACTER_ENCODING))
                time.sleep(duration)
            except KeyboardInterrupt:
                elapsed = time.time() - start
                sys.exit('{newline}{elapsed}'.format(newline=CRLF, elapsed=elapsed))
