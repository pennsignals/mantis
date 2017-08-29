import json
import os
import ssl
import sys
import tempfile
import time

from urllib.parse import urlparse
from urllib.request import build_opener, HTTPSHandler, Request, urlopen

from . import CRLF, DEFAULT_CHARACTER_ENCODING
from .command import HTTPCommand, RequestInvoker
from .handler import DefaultRequestHandler
from .loader import DefaultPackageLoader
from .publisher import Publisher

context = ssl.create_default_context()


def initialize():
    address = '{VAULT_ADDR}/v1/secret/password'.format(VAULT_ADDR=os.environ['VAULT_ADDR'])
    request = Request(address, headers={'X-Vault-Token': os.environ['VAULT_TOKEN']})
    with urlopen(request) as response, tempfile.NamedTemporaryFile() as f:
        value = json.loads(response.read().decode(DEFAULT_CHARACTER_ENCODING))['data']['value']
        f.write(value.encode(DEFAULT_CHARACTER_ENCODING))
        f.seek(0)
        context.load_cert_chain(f.name)


class Requester:

    DEFAULT_TIMEOUT_INTERVAL = 10

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
        self.publisher = Publisher()
        self.loader = DefaultPackageLoader()

    def request(self, duration=DEFAULT_TIMEOUT_INTERVAL):
        start = time.time()
        initialize()
        arguments = self.arguments
        identifier = urlparse(arguments.address)
        path = self.loader.specification.paths[identifier.path]
        operation = getattr(path, arguments.request.lower())
        # TODO: Separate OpenAPI bootstrapping functionality
        handler = self.loader.module.__dict__.get(
            operation.__dict__.get('x_request_handler', DefaultRequestHandler)
        )
        cls = type(handler.__class__.__name__, (handler, DefaultRequestHandler), {})
        invoker = RequestInvoker()
        invoker.register('onRequest', cls())
        while True:
            try:
                command = HTTPCommand(
                    Request(arguments.address, headers=arguments.header, method=arguments.request),
                    build_opener(HTTPSHandler(context=context))
                )
                invoker('onRequest', command)
                self.publisher(message=command.response.body)
                time.sleep(duration)
            except KeyboardInterrupt:
                elapsed = time.time() - start
                sys.exit('{newline}{elapsed}'.format(newline=CRLF, elapsed=elapsed))
