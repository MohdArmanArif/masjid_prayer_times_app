import sys
from fontmanager import FontManager
from datetime import datetime
from zoneinfo import ZoneInfo

from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QHeaderView, QLabel
)
from PyQt6.QtGui import QPainter, QPixmap, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QRect, QTimer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Waqt App")

        # Load background image (used in paintEvent)
        self.background_image = QPixmap("background.jpg")

        # Load fonts into script
        self.font_manager = FontManager("fonts")

        # Resize window to match image size
        self.resize(self.background_image.size())

        # Main layout splits screen LEFT ↔ RIGHT
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Left side = clock + table (stacked vertically)
        left_side_layout = QVBoxLayout()

        # Right side = reserved for future content (e.g. images)
        right_side_layout = QVBoxLayout()

        # ---------------- TABLE SETUP ----------------
        self.prayer_table = QTableWidget(6, 4)
        self.setup_table()

        # ---------------- CLOCK SETUP ----------------
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Style the clock text
        self.clock_label.setFont(
            self.font_manager.get_font("SF Mono", 120, bold=True)
        )

        # Define timezone (handles DST automatically)
        self.timezone = ZoneInfo("America/Toronto")

        # Set initial time immediately
        self.update_clock()

        # Timer updates the clock every 1 second
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        # ---------------- LAYOUT STRUCTURE ----------------

        # Left side layout:
        # Clock gets 1 part, table gets 4 parts (vertical split)
        left_side_layout.addWidget(self.clock_label, 1)
        left_side_layout.addWidget(self.prayer_table, 4)

        # Main layout:
        # Left side gets 3 parts, right side gets 2 parts (horizontal split)
        main_layout.addLayout(left_side_layout, 3)
        main_layout.addLayout(right_side_layout, 2)

    def setup_table(self):
        """
        Configures the prayer table appearance and fills it with data.
        """

        # Hide default row/column headers (numbers/letters)
        self.prayer_table.verticalHeader().setVisible(False)
        self.prayer_table.horizontalHeader().setVisible(False)

        # Style the table (glass effect + gold border)
        self.prayer_table.setStyleSheet("""
            QTableWidget {
                background: rgba(0, 120, 255, 25);
                border: 10px solid rgba(255, 215, 100, 150);
                border-radius: 25px;
                gridline-color: rgba(255, 215, 100, 50);
                color: rgba(255, 255, 255, 230);
                font-size: 40px;
            }

            QTableWidget::item {
                background: transparent;
                border: none;
                padding: 12px;
            }
        """)

        # Show grid lines but remove default frame
        self.prayer_table.setShowGrid(True)
        self.prayer_table.setFrameShape(self.prayer_table.Shape.NoFrame)

        # Make all cells stretch evenly to fill available space
        self.prayer_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prayer_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Sample data (can later be replaced with real data)
        table_data = [
            ["Prayer", "Start Time", "Iqaamah", "From..."],
            ["Fajr", "5:30 AM", "5:45 AM", "5:45 AM"],
            ["Dhuhr", "1:15 PM", "1:30 PM", "1:30 PM"],
            ["Asr", "5:00 PM", "5:20 PM", "5:20 PM"],
            ["Maghrib", "7:40 PM", "7:45 PM", "7:45 PM"],
            ["Isha", "9:00 PM", "9:15 PM", "9:15 PM"],
        ]

        # Populate the table
        for row in range(6):
            for col in range(4):
                cell = QTableWidgetItem(table_data[row][col])
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.prayer_table.setItem(row, col, cell)

    def paintEvent(self, event):
        """
        Draws the background image behind everything.
        Keeps aspect ratio and crops nicely.
        """
        painter = QPainter(self)

        if not self.background_image.isNull():
            window_rect = self.rect()

            # Scale image while keeping aspect ratio
            scaled_image = self.background_image.scaled(
                window_rect.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            # Center-crop the image
            x_offset = (scaled_image.width() - window_rect.width()) // 2
            y_offset = (scaled_image.height() - window_rect.height()) // 2

            source_rect = QRect(
                x_offset, y_offset,
                window_rect.width(),
                window_rect.height()
            )

            painter.drawPixmap(window_rect, scaled_image, source_rect)

    def update_clock(self):
        """
        Updates the clock label using the selected timezone.
        Automatically respects DST.
        """
        current_time = datetime.now(self.timezone)
        self.clock_label.setText(current_time.strftime("%I:%M:%S %p"))


# ---------------- APP ENTRY POINT ----------------

app = QApplication(sys.argv)
window = MainWindow()

# Fullscreen flag (currently both branches fullscreen — likely intentional for display)
if "--full" in sys.argv:
    window.showFullScreen()
else:
    window.showFullScreen()

app.exec()