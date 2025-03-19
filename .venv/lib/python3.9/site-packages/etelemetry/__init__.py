from .client import get_project, check_available_version, BadVersionError

from . import _version
__version__ = _version.get_versions()['version']
