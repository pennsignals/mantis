import logging  # noqa: E402
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)  # noqa: E402

import urllib.request

from urllib.parse import urlparse

from .handler import DefaultRequestHandler


class Command:

    def __call__(self):
        raise NotImplementedError()


class RequestInvoker:

    MAX_HISTORY = 10

    def __init__(self, max_history=MAX_HISTORY):
        self.history = []
        self.max_history = max_history
        self.handlers = {}

    def register(self, event, handler):
        self.handlers[event] = handler

    def __call__(self, event, command):
        invoker = self
        if len(invoker.history) >= invoker.max_history:
            invoker.history.pop(0)
        # Object must be copied following execution
        invoker.history.append(command)
        handler = invoker.handlers.get(event, DefaultRequestHandler())
        handler(command)


class HTTPCommand(Command):

    def __init__(self, request, opener=None):
        self.request = request
        self.response = None
        if opener is None:
            opener = urllib.request.build_opener()
        self.opener = opener

    def __call__(self):
        command = self
        with command.opener.open(command.request) as response:
            response.body = response.read()
        command.response = response
        assert response.closed
        identifier = urlparse(command.request.full_url)
        logging.info('* Connected to %s', identifier.netloc)
        logging.info('> %s %s %d', response._method, identifier.path, response.version)
        logging.info('> Host: %s', identifier.netloc)
        logging.info('>')
        logging.info('< Server: %s', response.getheader('Server'))
        logging.info('< Date: %s', response.getheader('Date'))
        logging.info('< Content-Type: %s', response.getheader('Content-Type'))
        logging.info('< Content-Length: %s', response.getheader('Content-Length'))
        logging.info('< Connection: %s', response.getheader('Connection'))
        logging.info('<')
        logging.info('* Connection #0 to host %s left intact', identifier.netloc)
