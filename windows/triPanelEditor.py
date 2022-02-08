import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QLabel, QSplitter, QVBoxLayout, QWidget

from widgets.hierarchyView import HierarchyView
from widgets.documentView import DocumentView


class TriPanelEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.docs = {}
        self.song_path = "./docs/"
        self.inventory_path = "./docs/inventory.txt"

        self.loaded = ""
        self.loaded_code = ""
        self.loaded_path = ""

        self.load()

        ftr_ht = 20

        self.info_view = QLabel(text="Information")

        self.setStyleSheet("""
            background: #30343b;
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.split_layout = QSplitter(Qt.Horizontal)
        self.split_layout.setContentsMargins(0, 0, 0, 0)

        # Hierarchy
        self.hrc_view = HierarchyView(self.docs, self.load_document)
        self.hrc_view.setMinimumWidth(75)
        self.hrc_view.setMaximumWidth(int(self.width() * 0.4))
        self.hrc_view.setStyleSheet("""
            background: #44484f;
            border-radius: 6px;
        """)

        self.split_layout.addWidget(self.hrc_view)
        self.split_layout.setCollapsible(0, False)

        # Document
        self.doc_view = DocumentView()
        self.doc_view.setMinimumWidth(500)
        self.doc_view.setStyleSheet("""
            background: #44484f;
            border-radius: 6px;
        """)
        self.split_layout.addWidget(self.doc_view)

        # Information
        self.split_layout.addWidget(self.info_view)
        self.split_layout.setSizes([
            250,
            (self.width() - 250) * 0.6,
            (self.width() - 250) * 0.4
        ])
        self.layout.addWidget(self.split_layout)

        # footer
        self.footer = QLabel(text="Footer")
        self.footer.setFixedSize(self.width(), ftr_ht)
        self.footer.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.footer)
        self.layout.setStretch(0, 1)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.hrc_view.setMaximumWidth(event.size().width() * 0.4)

        self.split_layout.setSizes([
            a := 350,
            (self.width() - a) * 0.6,
            (self.width() - a) * 0.4
        ])

    def load(self):
        temp = {}
        if not os.path.isdir(self.song_path):
            os.mkdir(self.song_path)

        if not os.path.isfile(self.inventory_path):
            with open(self.inventory_path, 'w') as _:
                pass  # Create File

        with open(self.inventory_path) as inv_file:
            lines = inv_file.read().splitlines()
            for line in lines:
                code, *name, path = line.split(", ")
                name = ", ".join(name)
                if code not in temp:
                    temp[code] = {}

                orig = name
                co = 1
                while name in temp:
                    name = f"{orig}{co}"
                    co += 1

                temp[code][name] = path

        self.docs = temp

    def load_document(self, code, name, path):
        self.loaded = name
        self.loaded_code = code
        self.loaded_path = path
        self.doc_view.load(code, name, path)
