# -*- coding: utf-8 -*-
#-----------------------------------------------------------
# 
# Points2One
# Copyright (C) 2010 Pavol Kapusta <pavol.kapusta@gmail.com>
# Copyright (C) 2010, 2013, 2015 Goyo <goyodiaz@gmail.com>
#-----------------------------------------------------------
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
#---------------------------------------------------------------------

from itertools import groupby
from os.path import basename
from os.path import dirname
from os.path import splitext
from os.path import join

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *
from qgis.PyQt import uic

from .p2o_encodings import getEncodings, getDefaultEncoding, setDefaultEncoding
from .p2o_engine import Engine, P2OError

BASE_FORM_CLASS, _ = uic.loadUiType(join(dirname(__file__), 'frmPoints2One.ui'))


class points2One(QDialog, BASE_FORM_CLASS):
    def __init__(self, iface):
        super(points2One, self).__init__()
        self.iface = iface
        self.setupUi(self)
        self.wInputLayer.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.wBrowse.clicked.connect(self.outFile)
        self.wSort1.toggled.connect(self.sort1_toggled)
        for combo in (self.wGroupField, self.wSortField1, self.wSortField2):
            combo.setLayer(self.layer())
            combo.setCurrentIndex(0)
        self.populate_encodings(getEncodings())
        self.show()

    def layer_name(self):
        """Return the selected input layer name as unicode."""
        return str(self.wInputLayer.currentText())

    def layer(self):
        """Return the selected input layer as a QgsMapLayer instance."""
        return self.wInputLayer.currentLayer()

    def output_geometry(self):
        """Return the selected output geometry."""
        if self.wCreateLines.isChecked():
            return QgsWkbTypes.LineString
        else:
            return QgsWkbTypes.Polygon

    def close_lines(self):
        """Return whether lines must be closed."""
        return self.wCloseLines.isChecked()

    def group(self):
        """Return whether grouping by attribute is enabled."""
        return self.wGroup.isChecked()

    def group_field(self):
        """Return the name of the grouping field."""
        if self.group():
            return str(self.wGroupField.currentText())

    def sort_fields(self):
        """Return the names of sorting fields as a list."""
        fields = []
        if self.wSort1.isChecked():
            fields.append(str(self.wSortField1.currentText()))
        if self.wSort2.isChecked():
            fields.append(str(self.wSortField2.currentText()))
        return fields


    def output_encoding(self):
        """Return the output encoding as unicode."""
        return str(self.wEncoding.currentText())

    def check_input(self):
        """Check whether the input is valid, raise if not."""
        layer = self.layer()
        if layer is None:
            msg = self.tr('Please select an input layer')
            raise P2OError(msg)

        if self.group_field() == '':
            msg = self.tr('Please select a field to group by')
            raise P2OError(msg)

        for field in self.sort_fields():
            if not field:
                msg = self.tr('Please select a field for sorting')
                raise P2OError(msg)

        if not self.output_path():
            msg = self.tr('Please specify output shapefile')
            raise P2OError(msg)

    def populate_encodings(self, names):
        """Populate the combo box of available encodings."""
        self.wEncoding.clear()
        self.wEncoding.addItems(names)
        index = self.wEncoding.findText(getDefaultEncoding())
        if index == -1:
            index = 0  # Make sure some encoding is selected.
        self.wEncoding.setCurrentIndex(index)

    def update_progress_bar(self):
        """Update the progress bar."""
        self.wProgressBar.setValue(self.wProgressBar.value() + 1)

    def _accept(self):
        self.check_input()
        layer = self.layer()
        self.wProgressBar.setRange(0, layer.dataProvider().featureCount())
        setDefaultEncoding(self.output_encoding())
        engine = Engine(
            layer,
            self.output_path(),
            self.output_encoding(),
            self.output_geometry(),
            self.close_lines(),
            self.group_field(),
            self.sort_fields(),
            self.update_progress_bar
        )

        engine.run()

        # Show warning
        log_msg = '\n'.join(engine.get_logger())
        if log_msg:
            warningBox = QMessageBox(self)
            warningBox.setWindowTitle('Points2One')
            message = self.tr('Output shapefile created')
            warningBox.setText(message)
            message = self.tr('There were some issues, maybe some features could not be created.')
            warningBox.setInformativeText(message)
            warningBox.setDetailedText(log_msg)
            warningBox.setIcon(QMessageBox.Warning)
            warningBox.exec_()

        if self.wAddResult.isChecked():
            addShapeToCanvas(str(self.output_path()))
        self.wProgressBar.setValue(0)

    def accept(self):
        try:
            self._accept()
        except P2OError as e:
            QMessageBox.critical(self, 'Points2One', str(e))

    def sort1_toggled(self, checked):
        if not checked:
            self.wSort2.setChecked(False)

    def outFile(self):
        """Open a file save dialog and set the output file path."""
        outFilePath = saveDialog(self)
        if not outFilePath:
            return
        self.setOutFilePath(outFilePath)

    def output_path(self):
        """Return the output file path."""
        return self.wOutputFileName.text()

    def setOutFilePath(self, outFilePath):
        """Set the output file path."""
        self.wOutputFileName.setText(outFilePath)


def saveDialog(parent):
    """Shows a save file dialog and return the selected file path."""
    settings = QSettings()
    key = '/UI/lastShapefileDir'
    outDir = settings.value(key)
    filter = 'Shapefiles (*.shp)'
    outFilePath, _ = QFileDialog.getSaveFileName(parent, parent.tr('Save output shapefile'), outDir, filter)
    outFilePath = str(outFilePath)
    if outFilePath:
        root, ext = splitext(outFilePath)
        if ext.upper() != '.SHP':
            outFilePath = f'{outFilePath}.shp'
        outDir = dirname(outFilePath)
        settings.setValue(key, outDir)
    return outFilePath


# Convenience function to add a vector layer to canvas based on input
# shapefile path (as string).
# Adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
def addShapeToCanvas(shapeFilePath):
    layerName = basename(shapeFilePath)
    root, ext = splitext(layerName)
    if ext == '.shp':
        layerName = root
    vlayer_new = QgsVectorLayer(shapeFilePath, layerName, "ogr")
    ret = QgsProject.instance().addMapLayer(vlayer_new)
    return ret
