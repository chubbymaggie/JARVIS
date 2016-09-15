#!/usr/bin/python
#
# Name: VulnDetectionWidget.py
# Description: It hosts all GUI elements relevant to vulnerability detection
#

from PySide import QtGui, QtCore
from PySide.QtGui import QIcon

from jarvis.widgets.CustomWidget import CustomWidget
import jarvis.core.helpers.BinaryEntropy as BE


#################################################################
class FirmwareWidget(CustomWidget):

    def __init__(self, parent = None):
        """
        Constructor
        """
        CustomWidget.__init__(self)
        self.name = "Firmware"
        self.parent = parent
        self.config = self.parent.config
        self.icon = QIcon(self.iconp + 'vuln_detection.png')
        self.img_data = None

        # Functionality associated with this widget
        self.binary_entropy = BE.BinaryEntropy()

        self._createGui()

    def _createGui(self):

        self._createToolBar('Firmware')
        self._createToolBarActions()

        self._createEntropyGraph()
        self._createOutputWindow()
        self._createOutputTable()

        # Output Layout
        self.splitter.addWidget(self.image_label)
        self.splitter.addWidget(self.image)
        self.splitter.addWidget(self.table_label)
        self.splitter.addWidget(self.table)
        self.splitter.addWidget(self.output_label)
        self.splitter.addWidget(self.output_window)

    def _createEntropyGraph(self):
        """
        Creates a clickable QPixmap
        """

        self.binary_entropy.calculate_entropy()
        self.binary_entropy.adjust_entropy_values()

        im_w = 200
        im_h = 200
        grid_size = self.binary_entropy.grid_size

        # Fastest way from array to string
        self.img_data = ''.join(self.binary_entropy.entropy_d.values())

        # Get QImage from QByteArray (from string)
        ba = QtCore.QByteArray.fromRawData(self.img_data)
        qi = QtGui.QImage(ba, grid_size, grid_size, QtGui.QImage.Format_RGB32)
        qi_scaled = qi.scaled(im_w, im_h, aspectMode = QtCore.Qt.KeepAspectRatio)

        # Get the QPixmap from a QImage
        qp = QtGui.QPixmap.fromImage(qi_scaled)

        # Apply the QPixmap to the label
        self.image = QtGui.QLabel()

        self.image.setPixmap(qp)
        self.image.setObjectName('Entropy')
        self.image.mousePressEvent = self._getPos

        self.image_label = QtGui.QLabel('Entropy Graph')

    def _getPos(self, event):
        """
        Gets the (x, y) position from
        clicking the image
        """
        x = event.pos().x()
        y = event.pos().y()

        print "(%d, %d)" % (x, y)
        self.binary_entropy.jump_to_bin_chunk(x, y)

    def _createToolBarActions(self):

        self.bannedAction = QtGui.QAction(
                QIcon(self.iconp + 'banned_ms_functions.png'),
                '&Usage of functions banned by Microsoft',
                self,
                triggered = self._notImplementedYet()
                )

        self.integerAction = QtGui.QAction(
                QIcon(self.iconp + 'integer_issues.png'),
                '&Search the whole binary for possible integer issues',
                self,
                triggered = self._notImplementedYet()
                )

        self.toolbar.addAction(self.bannedAction)
        self.toolbar.addAction(self.integerAction)

    #################################################################
    # GUI Callbacks
    #################################################################

    def _notImplementedYet(self):
        """
        Placeholder
        """
        pass
