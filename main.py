import sys
from Controller import Controller
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    controller = Controller()
    controller.show_login()

    sys.exit(app.exec_())