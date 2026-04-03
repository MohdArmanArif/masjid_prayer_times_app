import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHeaderView
)
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QRect


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Masjid App")

        # Load background image
        self.bg = QPixmap("background.jpg")

        # Make window start at the image's size/aspect ratio
        self.resize(self.bg.size())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 200, 700, 200)

        self.table = QTableWidget(6, 4)
        self.setup_table()

        layout.addWidget(self.table)

    def setup_table(self):
        # Hide row/column numbers
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        # Make table transparent except borders/grid/text
        self.table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                gridline-color: white;
                color: white;
                font-size: 40px;
                border: 10px solid white;
            }
            QTableWidget::item {
                background: transparent;
                border: none;
                padding: 8px;
            }
        """)

        self.table.setShowGrid(True)
        self.table.setFrameShape(self.table.Shape.NoFrame)

        # Make cells stretch evenly
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Sample text you can change later
        sample_data = [
            ["Prayer", "Start Time", "Iqaamah", "From..."],
            ["Fajr", "5:30 AM", "5:45 AM", "5:45 AM"],
            ["Dhuhr", "1:15 PM", "1:30 PM", "1:30 PM"],
            ["Asr", "5:00 PM", "5:20 PM", "5:20 PM"],
            ["Maghrib", "7:40 PM", "7:45 PM", "7:45 PM"],
            ["Isha", "9:00 PM", "9:15 PM", "9:15 PM"],
        ]

        for row in range(6):
            for col in range(4):
                item = QTableWidgetItem(sample_data[row][col])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

    def paintEvent(self, event):
        painter = QPainter(self)

        if not self.bg.isNull():
            window_rect = self.rect()
            scaled = self.bg.scaled(
                window_rect.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            x = (scaled.width() - window_rect.width()) // 2
            y = (scaled.height() - window_rect.height()) // 2

            source_rect = QRect(x, y, window_rect.width(), window_rect.height())
            painter.drawPixmap(window_rect, scaled, source_rect)


app = QApplication(sys.argv)
window = MainWindow()

if "--full" in sys.argv:
    window.showFullScreen()
else:
    window.show()

app.exec()