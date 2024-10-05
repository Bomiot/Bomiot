from os.path import dirname, exists
from os import makedirs
import logging
from bomiot import settings
import sys


def version():
    """
    get version from version file
    :return:
    """
    from bomiot import __version__
    return __version__.version()
