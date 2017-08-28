import json
import os
import re

from importlib.util import module_from_spec, spec_from_file_location

from .model import OpenAPI


class PackageLoader:

    def __call__(self):
        raise NotImplementedError()


class DefaultPackageLoader(PackageLoader):

    FILENAME = 'openapi.json'

    def __init__(self, path=os.getcwd, filename=FILENAME):
        filename = '{path}/{filename}'.format(path=path(), filename=filename)
        with open(filename) as f:
            instance = json.load(f)
        self.specification = OpenAPI.unmarshal(instance)
        expression = r'^(?P<module>handler[s]?)(?P<extension>\.py)$'
        module = None
        for _, _, filenames in os.walk(path()):
            for filename in filenames:
                match = re.match(expression, filename)
                if match is None:
                    continue
                # TODO: Error handling
                specification = spec_from_file_location(match.group('module'), match.string)
                module = module_from_spec(specification)
                specification.loader.exec_module(module)
                break
        self.module = module
