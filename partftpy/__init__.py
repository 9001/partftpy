# coding: utf-8
# vim: ts=4 sw=4 et ai:
from __future__ import print_function, unicode_literals

"""
This library implements the tftp protocol, based on rfc 1350.
http://www.faqs.org/rfcs/rfc1350.html
"""

import pkg_resources

from . import __name__ as pkg_name


def _get_version():
    try:
        pkg_version = pkg_resources.get_distribution(pkg_name).version
    except pkg_resources.DistributionNotFound:
        pkg_version = None
    return pkg_version


__version__ = _get_version()
