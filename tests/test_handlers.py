import unittest
import urllib.request

from mantis.handler import DefaultRequestHandler, RequestHandler

ADDRESS = 'https://api.spotify.com/v1/albums/{id}'.format(id='1Xdzq7uZAv640cXUoeAFAZ')


class CustomHandler(RequestHandler):

    def before_request(self, request):
        request.add_header('Content-Type', 'application/json')


class HandlerTestCase(unittest.TestCase):

    def runTest(self):
        request = urllib.request.Request(ADDRESS)
        handler = DefaultRequestHandler()
        handler.before_request(request)
        assert isinstance(request, urllib.request.Request)


class CustomHandlerTestCase(unittest.TestCase):

    def runTest(self):
        request = urllib.request.Request(ADDRESS)
        handler = CustomHandler()
        handler.before_request(request)
        assert request.has_header('Content-type')
        assert request.get_header('Content-type') == 'application/json'
