from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel


class HierarchyToolbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(28)

        self.setStyleSheet("background: #282c33;")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Default Layout
        self.toolbar = QWidget()
        self.toolbar_layout = QHBoxLayout(self.toolbar)
        self.toolbar_layout.setContentsMargins(6, 0, 6, 0)

        self.title = QLabel(text="Document Hierarchy")
        self.title.setFont(QFont('Calibri', 12))
        self.title.setStyleSheet("color: #8e8e8e;")
        self.toolbar_layout.addWidget(self.title)

        self.layout.addWidget(self.toolbar)
