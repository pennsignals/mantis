from pkg_resources import DistributionNotFound, get_distribution

DEFAULT_CHARACTER_ENCODING = 'UTF-8'
CRLF = '\r\n'

from .requester import Requester  # noqa: F401,E402

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass
