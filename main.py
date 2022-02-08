import sys
from PySide6.QtWidgets import QApplication

from windows.triPanelEditor import TriPanelEditor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Decodalyze")
    screenSize = app.primaryScreen().size()

    widget = TriPanelEditor()
    widget.resize(1080, 720)
    widget.showMaximized()

    sys.exit(app.exec())
