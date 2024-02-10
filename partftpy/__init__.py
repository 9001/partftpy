# vim: ts=4 sw=4 et ai:
"""
This library implements the tftp protocol, based on rfc 1350.
http://www.faqs.org/rfcs/rfc1350.html
"""

import sys

import pkg_resources

# Make sure that this is at least Python 3
required_version = (3, 0)
if sys.version_info < required_version:
    raise ImportError("Requires at least Python 3.0")

from . import TftpContexts, TftpPacketFactory, TftpPacketTypes, TftpStates
from . import __name__ as pkg_name
from .TftpClient import TftpClient
from .TftpServer import TftpServer
from .TftpShared import *


def _get_version():
    try:
        pkg_version = pkg_resources.get_distribution(pkg_name).version
    except pkg_resources.DistributionNotFound:
        pkg_version = None
    return pkg_version


__version__ = _get_version()
