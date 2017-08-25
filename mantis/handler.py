import logging


class Component:

    pass


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


class DefaultRequestHandler(RequestHandler):

    DEFAULT_CHARACTER_ENCODING = 'UTF-8'

    def __init__(self, encoding=DEFAULT_CHARACTER_ENCODING):
        self.encoding = encoding

    def before_request(self, request):
        pass

    def after_response(self, request, response):
        pass

    def after_error(self, request, response, e):
        logging.error(e)
