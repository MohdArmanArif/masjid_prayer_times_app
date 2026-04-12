import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from fontmanager import FontManager
from resource_path import resource_path
from time_data import PrayerDatabase

from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QHeaderView, QLabel
)
from PyQt6.QtGui import QPainter, QPixmap, QFont
from PyQt6.QtCore import Qt, QRect, QTimer


class DisplayWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Waqt Display")

        self.background_image = QPixmap(resource_path("background.jpg"))
        self.font_manager = FontManager(resource_path("fonts"))
        self.resize(self.background_image.size())

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)

        left_side_layout = QVBoxLayout()
        right_side_layout = QVBoxLayout()

        self.pd = PrayerDatabase()
        self.pd.load_data()

        self.prayer_table = QTableWidget(6, 4)
        self.jumuah_table = QTableWidget(2, 3)
        self.setup_tables()

        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self.font_manager.has_family("SF Mono"):
            clock_font = self.font_manager.get_font("SF Mono", 120, weight=700)
        else:
            clock_font = QFont()
            clock_font.setPointSize(40)

        self.clock_label.setFont(clock_font)

        self.timezone = ZoneInfo("America/Toronto")
        self.update_clock()

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        left_side_layout.addWidget(self.clock_label, 3)
        left_side_layout.addWidget(self.prayer_table, 12)
        left_side_layout.addWidget(self.jumuah_table, 4)

        main_layout.addLayout(left_side_layout, 3)
        main_layout.addLayout(right_side_layout, 2)

    def setup_tables(self):
        self.prayer_table.verticalHeader().setVisible(False)
        self.prayer_table.horizontalHeader().setVisible(False)
        self.jumuah_table.verticalHeader().setVisible(False)
        self.jumuah_table.horizontalHeader().setVisible(False)

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

        if self.font_manager.has_family("SF Pro Display"):
            table_font = self.font_manager.get_font("SF Pro Display", 40, weight=500)
        else:
            table_font = QFont()
            table_font.setPointSize(40)

        self.prayer_table.setFont(table_font)
        self.jumuah_table.setFont(table_font)

        self.prayer_table.setShowGrid(False)
        self.jumuah_table.setShowGrid(False)
        self.prayer_table.setFrameShape(self.prayer_table.Shape.NoFrame)
        self.jumuah_table.setFrameShape(self.jumuah_table.Shape.NoFrame)

        self.prayer_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.jumuah_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.prayer_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.jumuah_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        today_row = self.pd.get_today_row()

        prayer_table_data = [
            ["Prayer", "Start Time", "Iqaamah", "From..."],
            ["Fajr", today_row[1].strftime("%I:%M %p"), "5:45 AM", "5:45 AM"],
            ["Dhuhr", today_row[3].strftime("%I:%M %p"), "1:30 PM", "1:30 PM"],
            ["Asr", today_row[4].strftime("%I:%M %p"), "5:20 PM", "5:20 PM"],
            ["Maghrib", today_row[5].strftime("%I:%M %p"), "7:45 PM", "7:45 PM"],
            ["Isha", today_row[6].strftime("%I:%M %p"), "9:15 PM", "9:15 PM"],
        ]
        jumuah_table_data = [
            ["Jumuah", "1st Khutbah", "2nd Khutbah"],
            ["Times", "1:30 PM", "2:30 PM"],
        ]

        for row in range(6):
            for col in range(4):
                cell = QTableWidgetItem(prayer_table_data[row][col])
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.prayer_table.setItem(row, col, cell)

        for row in range(2):
            for col in range(3):
                cell = QTableWidgetItem(jumuah_table_data[row][col])
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.jumuah_table.setItem(row, col, cell)

    def paintEvent(self, event):
        painter = QPainter(self)

        if not self.background_image.isNull():
            window_rect = self.rect()

            scaled_image = self.background_image.scaled(
                window_rect.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            x_offset = (scaled_image.width() - window_rect.width()) // 2
            y_offset = (scaled_image.height() - window_rect.height()) // 2

            source_rect = QRect(
                x_offset, y_offset,
                window_rect.width(),
                window_rect.height()
            )

            painter.drawPixmap(window_rect, scaled_image, source_rect)

    def update_clock(self):
        current_time = datetime.now(self.timezone)
        self.clock_label.setText(current_time.strftime("%I:%M:%S %p"))


def run_display():
    app = QApplication(sys.argv)
    window = DisplayWindow()
    window.showFullScreen()
    app.exec()