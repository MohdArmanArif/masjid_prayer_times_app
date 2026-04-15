import sys

# Import PyQt6 widgets used in the launcher window
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

# Import the display window itself and the helper function
# run_display() starts the display as the main app window
# DisplayWindow lets us open the display directly from this launcher window
from display import DisplayWindow, run_display


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set launcher window title
        self.setWindowTitle("Waqt App")

        # Set initial launcher window size
        self.resize(400, 200)

        # Create the main vertical layout for this small launcher window
        layout = QVBoxLayout(self)

        # Create a button that opens the main display screen
        self.open_display_button = QPushButton("Open Display")
        self.open_display_button.clicked.connect(self.open_display)

        # Add the button to the layout
        layout.addWidget(self.open_display_button)

    def open_display(self):
        # Create the display window when the button is clicked
        # Store it on self so it does not get garbage-collected immediately
        self.display_window = DisplayWindow()

        # Show the display in fullscreen mode
        self.display_window.showFullScreen()


if __name__ == "__main__":
    # If the script is run with --display,
    # skip the launcher window and open the display directly
    if "--display" in sys.argv:
        run_display()

    # Otherwise, open the small launcher window
    else:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec()

        # Nextion displays
        # https://www.makerfabs.com/esp32-s3-parallel-tft-with-touch-7-inch.html
        # http://makercanada.ca/