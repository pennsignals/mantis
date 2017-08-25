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
        assert isinstance(schema.paths['/albums/{id}'], model.PathItem)
        assert isinstance(schema.paths['/albums/{id}'].get, model.Operation)


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
        assert hasattr(schema.paths['/albums/{id}'].get, 'x_request_handler')
