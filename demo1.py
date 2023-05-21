import sys
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QVBoxLayout


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('My Window')

        # 创建列表控件
        self.list_widget = QListWidget()
        self.list_widget.addItems(['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'])


        # 创建布局
        vbox = QVBoxLayout()
        vbox.addWidget(self.list_widget)

        # 设置主布局
        self.setLayout(vbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())
