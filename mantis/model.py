import re


class Component:

    def __init__(self, parent=None):
        self.parent = parent

    def accept(self, visitor):
        raise NotImplementedError()


class Extensible:

    """While the OpenAPI Specification tries to accommodate most use
    cases, additional data can be added to extend the specification at
    certain points.

    The extensions properties are implemented as patterned fields that
    are always prefixed by "x-".
    """

    def __init__(self, **kwargs):
        for name, member in kwargs.items():
            if re.search(r'^x-', name) is not None:
                name = name.replace('-', '_')
                setattr(self, name, member)


class OpenAPI(Extensible):

    """This is the root document object of the OpenAPI document.
    """

    def __init__(self, openapi='3.0.0', info=None, servers=None, paths=None, components=None,
                 security=None, tags=None, externalDocs=None, **kwargs):
        assert bool(openapi)
        super().__init__(**kwargs)
        self.openapi = openapi
        self.info = info
        self.servers = servers
        self.paths = paths
        self.components = components
        self.security = security
        self.tags = tags
        self.externalDocs = externalDocs

    @classmethod
    def unmarshal(cls, instance):
        instance = cls(**instance)
        instance.info = Info.unmarshal(instance.info)
        instance.servers = Servers.unmarshal(instance.servers)
        instance.paths = Paths.unmarshal(instance.paths)
        return instance


class Info(Extensible):

    """The object provides metadata about the API.
    """

    def __init__(self, title='', description='', termsOfService='', contact=None, license=None,
                 version='', **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.termsOfService = termsOfService
        self.contact = contact
        self.license = license
        self.version = version

    @classmethod
    def unmarshal(cls, instance):
        instance = cls(**instance)
        if instance.contact is None:
            instance.contact = {}
        instance.contact = Contact(**instance.contact)
        if instance.license is None:
            instance.license = {}
        instance.license = License(**instance.license)
        return instance


class Contact(Extensible):

    """Contact information for the exposed API.
    """

    def __init__(self, name='', url='', email='', **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.url = url
        self.email = email


class License(Extensible):

    """License information for the exposed API.
    """

    def __init__(self, name='', url='', **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.url = url


class Servers(list):

    @classmethod
    def unmarshal(cls, instance=None):
        if instance is None:
            # If the servers property is not provided, or is an empty
            # array, the default value would be a Server Object with a
            # url value of /.
            return cls([Server(url='/')])
        return cls(Server.unmarshal(element) for element in instance)


class Server(Extensible):

    """An object representing a Server.
    """

    def __init__(self, url='', description='', variables=None, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.description = description
        self.variables = variables

    @classmethod
    def unmarshal(cls, instance):
        return cls(**instance)


class Paths(dict):

    """Holds the relative paths to the individual endpoints and their
    operations. The path is appended to the URL from the Server Object
    in order to construct the full URL. The Paths MAY be empty, due to
    ACL constraints.
    """

    # TODO: Needs extensible

    @classmethod
    def unmarshal(cls, instance=None):
        if instance is None:
            instance = {}
        return cls({name: PathItem.unmarshal(member) for name, member in instance.items()})

    def accept(self, visitor):
        for member in self.values():
            member.accept(visitor)


class PathItem(Extensible):

    """Describes the operations available on a single path. A Path Item
    MAY be empty, due to ACL constraints. The path itself is still
    exposed to the documentation viewer but they will not know which
    operations and parameters are available.
    """

    def __init__(self, summary='', description='', get=None, put=None, post=None, delete=None,
                 options=None, head=None, patch=None, trace=None, servers=None, parameters=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.reference = kwargs.get('$ref', '')
        self.summary = summary
        self.get = get
        self.put = put
        self.post = post
        self.delete = delete
        self.options = options
        self.head = head
        self.patch = patch
        self.trace = trace
        self.servers = servers
        self.parameters = parameters

    @classmethod
    def unmarshal(cls, instance):
        instance = cls(**instance)
        for method in ('get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace',):
            operation = getattr(instance, method)
            if operation is None:
                operation = {}
            setattr(instance, method, Operation.unmarshal(operation))
        return instance

    def accept(self, visitor):
        visitor.visit_path(self)


class Operation(Extensible):

    """Describes a single API operation on a path.
    """

    def __init__(self, tags=None, summary='', description='', externalDocs=None, operationId='',
                 parameters=None, requestBody=None, responses=None, callbacks=None,
                 deprecated=False, security=None, servers=None, **kwargs):
        super().__init__(**kwargs)
        if tags is None:
            tags = []
        self.tags = list(set(tags))
        self.summary = summary
        self.description = description
        self.externalDocs = externalDocs
        self.operationId = operationId
        self.parameters = parameters
        self.requestBody = requestBody
        self.responses = responses
        self.callbacks = callbacks
        self.deprecated = deprecated
        self.security = security
        self.servers = servers

    @classmethod
    def unmarshal(cls, instance):
        instance = cls(**instance)
        instance.parameters = Parameters.unmarshal(instance.parameters)
        instance.responses = Responses.unmarshal(instance.responses)
        return instance


class Parameters(list):

    @classmethod
    def unmarshal(cls, instance=None):
        if instance is None:
            instance = []
        return cls(Parameter.unmarshal(element) for element in instance)


class Parameter(Extensible):

    """Describes a single operation parameter.
    """

    def __init__(self, name='', description='', required=False, deprecated=False,
                 allowEmptyValue=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        parameterIn = kwargs.get('in', '')
        self.parameterIn = parameterIn
        self.description = description
        self.required = required
        self.deprecated = deprecated
        self.allowEmptyValue = allowEmptyValue

    @classmethod
    def unmarshal(cls, instance):
        instance = cls(**instance)
        return instance


class MediaType(Extensible):

    def __init__(self, schema=None, example=None, examples=None, encoding=None, **kwargs):
        super().__init__(**kwargs)
        self.schema = schema
        self.example = example
        self.examples = examples
        self.encoding = encoding

    @classmethod
    def unmarshal(cls, instance):
        return cls(**instance)


class Responses(dict):

    """A container for the expected responses of an operation.
    The container maps a HTTP response code to the expected response.
    """

    def get(self, status, default='default'):
        # Alias the get method from the parent object
        get = super().get
        return get(str(status), get(default))

    @classmethod
    def unmarshal(cls, instance=None):
        if instance is None:
            instance = {}
        return cls({name: Response.unmarshal(member) for name, member in instance.items()})


class Response(Extensible):

    """Describes a single response from an API Operation,
    including design-time, static links to operations based on the
    response.
    """

    def __init__(self, description='', headers=None, content=None, links=None, **kwargs):
        super().__init__(**kwargs)
        self.description = description
        self.headers = headers
        self.content = content
        self.links = links

    @classmethod
    def unmarshal(cls, instance):
        instance = cls(**instance)
        if instance.content is None:
            instance.content = {}
        instance.content = {
            name: MediaType.unmarshal(member) for name, member in instance.content.items()
        }
        return instance
