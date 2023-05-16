import sys
from PyQt6.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt6.QtGui import QFont

class PyQt6Actions(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
    def main(self):
        app = QApplication(sys.argv)
        sys.exit(app.exec())
    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()




if __name__ == '__main__':
    PyQt6Actions().main()