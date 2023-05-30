from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    import objects
    import signals

    sys.exit(app.exec())
