from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QFont, QPixmap

from pathlib import Path

from matplotlib import image

class MuseItem(QtWidgets.QGroupBox):
    def __init__(self, parent=None, name="Muse Item ABCD", address="128080"):
        super().__init__(parent)
        # self.setTitle("Muse Item")
        self.setMinimumSize(300, 100)
        self.setMaximumSize(10000, 100)
        
        self.widgetLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.widgetLayout)
        
        self.titleWidget = QtWidgets.QWidget(self)
        self.titleLayouts = QtWidgets.QVBoxLayout()
        self.titleWidget.setLayout(self.titleLayouts)
        self.titleLayouts.setContentsMargins(10, 10, 10, 10)
        self.titleLayouts.setSpacing(10)
        
        self.nameLabel = QtWidgets.QLabel(name, self)
        self.nameLabel.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.addressLabel = QtWidgets.QLabel(address, self)
        self.addressLabel.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.titleLayouts.addWidget(self.nameLabel)
        self.titleLayouts.addWidget(self.addressLabel)
        
        self.rightButtonsWidget = QtWidgets.QWidget(self)
        self.rightButtonsLayout = QtWidgets.QVBoxLayout()
        self.rightButtonsLayout.setContentsMargins(0, 0, 0, 0)
        self.rightButtonsLayout.setSpacing(10)
        self.rightButtonsWidget.setLayout(self.rightButtonsLayout)
        
        self.connectButton = QtWidgets.QPushButton("Connect", self)
        self.connectButton.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.rightButtonsLayout.addWidget(self.connectButton)
        
        self.widgetLayout.addWidget(self.titleWidget)
        self.widgetLayout.addWidget(self.rightButtonsWidget)
        
    def set_title(self, title):
        self.setTitle(title)
    