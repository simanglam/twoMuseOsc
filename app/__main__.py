from PyQt6 import QtWidgets
from .window import MyWidget
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec())