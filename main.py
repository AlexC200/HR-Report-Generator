import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()  # student version does not have this
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
