import zmq


class Publisher:

    SCHEME = 'TCP'

    def __init__(self, scheme=SCHEME, host='*', port=1337):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind('{scheme}://{host}:{port}'.format(scheme=scheme.lower(), host=host, port=port))
        self.socket = socket

    def __call__(self, topic=b'onResponseReceived', message=b''):
        self.socket.send_multipart([topic, message])
