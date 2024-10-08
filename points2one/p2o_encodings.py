# -*- coding: utf-8 -*-

# Copyright 2010, 2013 Goyo <goyodiaz@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


"""Encoding related stuff."""

from qgis.PyQt.QtCore import QSettings, QTextCodec


def getEncodings():
    """Return a list of available encodings."""
    names = [
        bytes(QTextCodec.codecForMib(mib).name()).decode()
        for mib in QTextCodec.availableMibs()
    ]
    return names


def getDefaultEncoding(default="System"):
    """Return the default encoding."""
    settings = QSettings()
    encoding = settings.value("/UI/encoding", default)
    return encoding


def setDefaultEncoding(encoding):
    """Set the default encoding."""

    # Make sure encoding is not blank.
    encoding = encoding or "System"
    settings = QSettings()
    settings.setValue("/UI/encoding", encoding)
