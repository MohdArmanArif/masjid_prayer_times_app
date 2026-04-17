import sys
from datetime import datetime
from zoneinfo import ZoneInfo

# Import custom modules used by this window
# - FontManager loads custom fonts from the fonts folder
# - resource_path finds files correctly in dev mode and bundled app mode
# - PrayerDatabase fetches and prepares prayer time data
from fontmanager import FontManager
from resource_path import resource_path
from time_data import PrayerDatabase

# Import PyQt6 widgets and tools needed to build the UI
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QHeaderView, QLabel
)
from PyQt6.QtGui import QPainter, QPixmap, QFont
from PyQt6.QtCore import Qt, QRect, QTimer


class DisplayWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title shown by the operating system
        self.setWindowTitle("Waqt App")

        # Load the background image for the display window
        self.background_image = QPixmap(resource_path("background.jpg"))

        # Load all custom fonts from the fonts folder
        self.font_manager = FontManager(resource_path("fonts"))

        # Start the window at the same size as the background image
        self.resize(self.background_image.size())

        # Main layout splits the window into left and right sections
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Left side will contain the clock and tables
        left_side_layout = QVBoxLayout()

        # Right side is reserved for future content such as images or announcements
        right_side_layout = QVBoxLayout()

        # ---------------- DATA SETUP ----------------
        # Create the prayer database helper and load the prayer data
        self.pd = PrayerDatabase()
        self.pd.load_data()

        # ---------------- TABLE SETUP ----------------
        # Create the two tables used in the display
        self.prayer_table = QTableWidget(6, 4)
        self.jumuah_table = QTableWidget(2, 3)
        self.setup_tables()

        # ---------------- CLOCK SETUP ----------------
        # Create the label that will display the live clock
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Try to use the custom SF Mono font for the clock
        # If that font is not available, fall back to a normal Qt font
        if self.font_manager.has_family("SF Mono"):
            clock_font = self.font_manager.get_font("SF Mono", 120, weight=700)
        else:
            clock_font = QFont()
            clock_font.setPointSize(40)

        self.clock_label.setFont(clock_font)

        # Define the timezone used for the clock
        self.timezone = ZoneInfo("America/Toronto")

        # Set the clock text immediately when the window starts
        self.update_clock()

        # Create a timer to refresh the clock every 1 second
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        # ---------------- LAYOUT STRUCTURE ----------------
        # Add the clock and tables to the left side
        left_side_layout.addWidget(self.clock_label, 3)
        left_side_layout.addWidget(self.prayer_table, 12)
        left_side_layout.addWidget(self.jumuah_table, 4)

        # Add left and right sections to the main window
        main_layout.addLayout(left_side_layout, 3)
        main_layout.addLayout(right_side_layout, 2)

    def setup_tables(self):
        # Hide the default row and column headers on both tables
        self.prayer_table.verticalHeader().setVisible(False)
        self.prayer_table.horizontalHeader().setVisible(False)
        self.jumuah_table.verticalHeader().setVisible(False)
        self.jumuah_table.horizontalHeader().setVisible(False)

        # Shared stylesheet for both tables
        table_style = """
        QTableWidget {
            background: rgba(0, 120, 255, 25);
            border: 15px solid rgba(255, 215, 100, 200);
            border-radius: 25px;
            gridline-color: rgba(255, 215, 100, 50);
            color: rgba(255, 255, 255, 230);
        }

        QTableWidget::item {
            background: transparent;
            border: 1px solid rgba(255, 215, 100, 50);
            padding: 12px;
        }
        """
        self.prayer_table.setStyleSheet(table_style)
        self.jumuah_table.setStyleSheet(table_style)

        # Try to use the custom SF Pro Display font for the tables
        if self.font_manager.has_family("SF Pro Display"):
            table_font = self.font_manager.get_font("SF Pro Display", 40, weight=500)
        else:
            table_font = QFont()
            table_font.setPointSize(40)

        self.prayer_table.setFont(table_font)
        self.jumuah_table.setFont(table_font)

        # Turn off the built-in Qt grid lines and remove the default widget frame
        self.prayer_table.setShowGrid(False)
        self.jumuah_table.setShowGrid(False)
        self.prayer_table.setFrameShape(self.prayer_table.Shape.NoFrame)
        self.jumuah_table.setFrameShape(self.jumuah_table.Shape.NoFrame)

        # Make all rows and columns stretch evenly to fill the available table space
        self.prayer_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.jumuah_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prayer_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.jumuah_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Ask the prayer database for today's prayer row
        today_row = self.pd.get_today_row()

        # Build the data used to fill the main prayer table
        prayer_table_data = [
            ["Prayer", "Start Time", "Iqaamah", "From..."],
            ["Fajr", today_row["fajr"].strftime("%I:%M %p"), "5:45 AM", "5:45 AM"],
            ["Dhuhr", today_row["dhuhr"].strftime("%I:%M %p"), "1:30 PM", "1:30 PM"],
            ["Asr", today_row["asr"].strftime("%I:%M %p"), "5:20 PM", "5:20 PM"],
            ["Maghrib", today_row["maghrib"].strftime("%I:%M %p"), "7:45 PM", "7:45 PM"],
            ["Isha", today_row["isha"].strftime("%I:%M %p"), "9:15 PM", "9:15 PM"],
        ]

        # Build the data used to fill the Jumuah table
        jumuah_table_data = [
            ["Jumuah", "1st Khutbah", "2nd Khutbah"],
            ["Times", "1:30 PM", "2:30 PM"],
        ]

        # Fill the prayer table cell-by-cell
        for row in range(6):
            for col in range(4):
                cell = QTableWidgetItem(prayer_table_data[row][col])
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.prayer_table.setItem(row, col, cell)

        # Fill the Jumuah table cell-by-cell
        for row in range(2):
            for col in range(3):
                cell = QTableWidgetItem(jumuah_table_data[row][col])
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.jumuah_table.setItem(row, col, cell)

    def paintEvent(self, event):
        # This custom paint method draws the background image behind the widgets
        painter = QPainter(self)

        if not self.background_image.isNull():
            window_rect = self.rect()

            # Scale the image so it fully covers the window
            # KeepAspectRatioByExpanding preserves aspect ratio while filling the space
            scaled_image = self.background_image.scaled(
                window_rect.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            # Calculate how much of the scaled image needs to be cropped
            x_offset = (scaled_image.width() - window_rect.width()) // 2
            y_offset = (scaled_image.height() - window_rect.height()) // 2

            # Define the source area to crop from the scaled image
            source_rect = QRect(
                x_offset, y_offset,
                window_rect.width(),
                window_rect.height()
            )

            # Draw the cropped, scaled background image into the window
            painter.drawPixmap(window_rect, scaled_image, source_rect)

    def update_clock(self):
        # Get the current time using the selected timezone
        current_time = datetime.now(self.timezone)

        # Format the time as HH:MM:SS AM/PM and display it on the label
        self.clock_label.setText(current_time.strftime("%I:%M:%S %p"))


def run_display(fullscreen=False):
    # Create the Qt application object
    app = QApplication(sys.argv)

    # Create the display window
    window = DisplayWindow()

    # Show the window either fullscreen or normal size
    if fullscreen:
        window.showFullScreen()
    else:
        window.show()

    # Start the Qt event loop
    app.exec()