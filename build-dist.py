#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010-2015 Goyo <goyodiaz@gmail.com>
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

# XXX Should use make for this?

"""Build a zip file for distribution.

See http://pyqgis.org/admin/contributed/python_plugins/packaging for
packaging guidelines.

"""

import os
import zipfile as zip

dirs = {
    '': ([
        'LICENSE.txt'],
        'points2one'),
    'points2one': ([
        'frmPoints2One.ui',
        'about_dialog_base.ui',
        'about_dialog.py',
        'metadata.txt',
        '__init__.py',
        'p2o_encodings.py',
        'p2o_engine.py',
        'p2o_errors.py',
        'points2one.png',
        'points2one_gui.py',
        'points2one_plugin.py',
                   ],
        'points2one'),
    'points2one/i18n': ([
        'points2one_es_ES.ts',
        'points2one_es_ES.qm',
        'points2one_fr_FR.ts',
        'points2one_fr_FR.qm',
        'points2one_ru_RU.ts',
        'points2one_ru_RU.qm'],
        os.path.join('points2one', 'i18n'))}

zipfile = zip.ZipFile('points2one.zip', mode='w')
for dirname in dirs:
    destdir = dirs[dirname][1]
    for fname in dirs[dirname][0]:
        zipfile.write(os.path.join(dirname, fname),
                      os.path.join(destdir, fname))
zipfile.close()
