# -----------------------------------------------------------
# 
# Points2One
# Copyright (C) 2010-2011 Pavol Kapusta <pavol.kapusta@gmail.com>
# Copyright (C) 2011, 2013 Goyo <goyodiaz@gmail.com>
# 
# -----------------------------------------------------------
# 
# licensed under the terms of GNU GPL 2
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
# 
# ---------------------------------------------------------------------

import os
from os import path

from qgis.PyQt.QtCore import *
# from qgis.PyQt.QtCore import QgsApplication
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtCore import QTranslator, QCoreApplication
from .points2one_gui import points2One

from . import about_dialog


class points2one(object):
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = path.dirname(__file__)
        self._translator = None
        self.__init_translator()

    # def load_translation(self):
    #     ## Initialize the translation environment.
    #     locale = QSettings().value('locale/userLocale')
    #     filepath = str(__file__)
    #     locale_path = os.path.join(os.path.dirname(filepath), 'i18n',
    #                                ''.join(['points2one_', locale, '.qm']))
    #     if QFileInfo(locale_path).exists():
    #         self.translator = QTranslator()
    #         self.translator.load(locale_path)
    #         if qVersion() > '4.3.3':
    #             QCoreApplication.installTranslator(self.translator)

    def __init_translator(self):
        # initialize locale
        locale = QSettings().value('locale/userLocale')

        def add_translator(locale_path):
            if not path.exists(locale_path):
                return
            translator = QTranslator()
            translator.load(locale_path)
            QCoreApplication.installTranslator(translator)
            self._translator = translator  # Should be kept in memory

        add_translator(path.join(
            self.plugin_dir, 'i18n',
            'points2one_{}_{}.qm'.format(locale, locale.upper())
        ))

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        # create action
        _current_path = os.path.abspath(os.path.dirname(__file__))
        plugin_icon_path = os.path.abspath(os.path.join(_current_path, 'points2one.png'))
        plugin_icon = QIcon(plugin_icon_path)

        self.action = QAction(
            plugin_icon, 'Points2One', self.iface.mainWindow()
        )
        self.action.setWhatsThis('Create polygons and lines from vertices.')
        self.action.triggered.connect(self.run)
        self.actionAbout = QAction(self.tr('About'), self.iface.mainWindow())
        self.actionAbout.triggered.connect(self.about)
        # add toolbar button and menu item
        self.iface.addVectorToolBarIcon(self.action)
        self.iface.addPluginToVectorMenu('&Points2One', self.action)
        self.iface.addPluginToVectorMenu('&Points2One', self.actionAbout)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginVectorMenu('&Points2One', self.action)
        self.iface.removePluginVectorMenu('&Points2One', self.actionAbout)
        self.iface.removeVectorToolBarIcon(self.action)

    def run(self):
        dialog = points2One(self.iface)
        dialog.exec_()

    def about(self):
        dialog = about_dialog.AboutDialog(os.path.basename(self.plugin_dir))
        dialog.exec_()

    def tr(self, message):
        return QCoreApplication.translate(__class__.__name__, message)
