import json
import os
import unittest

from unittest.mock import patch, PropertyMock

from mantis import model


class ResponseVisitorTestCase(unittest.TestCase):

    @patch('http.client.HTTPResponse')
    @patch('urllib.request.Request')
    def runTest(self, request, response):
        with open(os.path.join(os.path.dirname(__file__), 'openapi.json')) as fp:
            instance = json.load(fp)
        specification = model.OpenAPI.unmarshal(instance)
        address = 'https://api.spotify.com/v1/albums/6s86NPxqYeeU3BB6siMkyR'

        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.PropertyMock
        #
        # Because of the way mock attributes are stored you can’t
        # directly attach a PropertyMock to a mock object.
        type(request).full_url = PropertyMock(return_value=address)
        type(response).status = PropertyMock(return_value=200)
        response.getheader.return_value = 'application/json'

        default = specification.paths['/v1/albums/{id}'].get.responses.get(response.status)
        schema = default.content.get(response.getheader('content-type')).schema
        response.getheader.assert_called_with('content-type')
        assert isinstance(default, model.Response)
        assert schema['$ref'] == '#/components/schemas/AlbumFull'
