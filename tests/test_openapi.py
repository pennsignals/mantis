import json
import os
import unittest

from mantis import model


class BaseTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(os.path.join(os.path.dirname(__file__), 'openapi.json')) as fp:
            instance = json.load(fp)
        self.instance = instance


class OpenAPITestCase(BaseTestCase):

    def runTest(self):
        instance = self.instance
        schema = model.OpenAPI.unmarshal(instance)
        assert schema.openapi == '3.0.0'
        assert isinstance(schema.info.contact, model.Contact)
        assert isinstance(schema.info.license, model.License)
        assert isinstance(schema.servers, model.Servers)
        assert isinstance(schema.paths, model.Paths)
        path = schema.paths['/v1/albums/{id}']
        assert isinstance(path, model.PathItem)
        assert isinstance(path.get, model.Operation)
        assert isinstance(path.get.responses, model.Responses)
        assert isinstance(path.get.responses['200'], model.Response)


class DefaultServersTestCase(BaseTestCase):

    def runTest(self):
        instance = self.instance
        instance.pop('servers')
        schema = model.OpenAPI.unmarshal(instance)
        assert len(schema.servers) == 1
        assert schema.servers[0].url == '/'


class SpecificationExtensionsTestCase(BaseTestCase):

    def runTest(self):
        instance = self.instance
        schema = model.OpenAPI.unmarshal(instance)
        assert hasattr(schema.paths['/v1/albums/{id}'].get, 'x_request_handler')
