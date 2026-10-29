from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from narwhals import Unknown


from muselsl import stream, list_muses

class Worker(QThread):
    result_ready = pyqtSignal(list)  # 定義一個 Signal，傳遞字典列表

    def run(self):
        muses = list_muses()
        if (muses is not None) and (len(muses) > 0):
            self.result_ready.emit([(muse["name"], muse["address"]) for muse in muses])
        else:
            self.result_ready.emit([])
