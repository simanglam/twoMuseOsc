from PyQt6 import QtWidgets
from .mainWindow import MainWindow
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MainWindow()
    Form.show()
    sys.exit(app.exec())