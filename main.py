import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

from display import DisplayWindow, run_display


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Waqt App")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        self.open_display_button = QPushButton("Open Display")
        self.open_display_button.clicked.connect(self.open_display)

        layout.addWidget(self.open_display_button)

    def open_display(self):
        self.display_window = DisplayWindow()
        self.display_window.showFullScreen()


if __name__ == "__main__":
    if "--display" in sys.argv:
        run_display()
    else:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()