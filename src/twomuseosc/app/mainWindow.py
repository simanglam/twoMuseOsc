from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtGui import QFont, QPixmap
from narwhals import Unknown
from .museItem import MuseItem

from .museScanWorker import Worker


import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TwoMuseOSC")
        self.setGeometry(100, 100, 400, 300)
        self.layouts = QtWidgets.QVBoxLayout()
        self.layouts.setContentsMargins(10, 10, 10, 10)
        
        self.setLayout(self.layouts)
        
        self.layouts.addWidget(MuseItem(self))
        
        self.worker = Worker()
        self.worker.result_ready.connect(self.update_label)
        self.worker.start()



    @QtCore.pyqtSlot(list)  # 定義一個 Slot，接收字典列表
    def update_label(self, muses: list[tuple[str, str]]):
        for i in reversed(range(self.layouts.count())):
            widget = self.layouts.itemAt(i)
            if widget is not None:
                widget = widget.widget()
            if widget is not None:
                widget.setParent(None)
        if (muses is not None) and (len(muses) > 0):
            for muse in muses:
                self.layouts.addWidget(MuseItem(self, name=muse[0], address=muse[1]))
        
        else:
            self.layouts.addWidget(QtWidgets.QLabel("找不到 Muse 裝置，請確認 Muse 是否已開啟並配對。", self))