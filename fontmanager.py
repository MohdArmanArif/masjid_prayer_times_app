import os
from PyQt6.QtGui import QFont, QFontDatabase


class FontManager:
    def __init__(self, fonts_folder="fonts"):
        # Get the directory where THIS Python file lives
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Build absolute path to fonts folder
        self.fonts_folder = os.path.join(script_dir, fonts_folder)

        self.loaded_families = set()
        self.load_all_fonts()

    def load_all_fonts(self):
        """
        Load every .otf and .ttf file in the fonts folder into the app.
        This makes the fonts available even if they are not installed system-wide.
        """
        if not os.path.exists(self.fonts_folder):
            print(f"Fonts folder not found: {self.fonts_folder}")
            return

        for file_name in os.listdir(self.fonts_folder):

            # Skip macOS metadata files
            if file_name.startswith("._"):
                continue

            if file_name.lower().endswith((".otf", ".ttf")):
                file_path = os.path.join(self.fonts_folder, file_name)
                font_id = QFontDatabase.addApplicationFont(file_path)

                if font_id == -1:
                    print(f"Failed to load font: {file_path}")
                    continue

                families = QFontDatabase.applicationFontFamilies(font_id)
                for family in families:
                    self.loaded_families.add(family)
                    print(f"Loaded font family: {family}")

    def get_font(self, family_name, point_size, bold=False, italic=False):
        """
        Create a QFont from a loaded family name.
        If that family was not loaded, Qt will try to fall back gracefully.
        """
        font = QFont(family_name, point_size)
        font.setBold(bold)
        font.setItalic(italic)
        return font

    def has_family(self, family_name):
        return family_name in self.loaded_families