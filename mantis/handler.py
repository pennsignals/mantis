import logging  # noqa: E402
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)  # noqa: E402

from . import DEFAULT_CHARACTER_ENCODING


class RequestHandler:

    def before_request(self, request):
        """Runs any additional processing logic on the specified request
        (before it is executed by the client runtime).
        """
        raise NotImplementedError()

    def after_response(self, request, response):
        """Runs any additional processing logic on the specified request
        (after is has been executed by the client runtime).
        """
        raise NotImplementedError()

    def after_error(self, request, response, e):
        """Runs any additional processing logic on a request after
        it has failed.
        """
        raise NotImplementedError()

    def __call__(self, command):
        self.before_request(command.request)
        command()
        self.after_response(command.request, command.response)


class DefaultRequestHandler(RequestHandler):

    def __init__(self, encoding=DEFAULT_CHARACTER_ENCODING):
        self.encoding = encoding

    def before_request(self, request):
        logging.info(request)

    def after_response(self, request, response):
        logging.info(response)

    def after_error(self, request, response, e):
        pass
