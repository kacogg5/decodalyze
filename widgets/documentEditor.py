from PySide6.QtCore import Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy


class EditorLine(QWidget):
    def __init__(self, text):
        super().__init__()
        self.content = text

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 0, 0, 1)

        self.content_label = QLabel(text=self.content)
        self.content_label.setWordWrap(True)
        self.content_label.setAlignment(Qt.AlignTop)
        self.content_label.setStyleSheet("""
            background: transparent;
            color: #8e8e8e;
            font-family: 'Lucida Console';
            font-size: 12px;
            border-radius: 0;
            padding: 0 2px 0 0;
        """)

        self.layout.addWidget(self.content_label)


class EnhancedEditorLine(QWidget):
    def __init__(self, lang_a, lang_b):
        super().__init__()


class DocumentEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.path = ""

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        mw = 50
        self.numbers = []
        self.lines = []

        self.content = [
            "No document has been selected.",
            "Open a file from the menu on the left."
        ]

        for n, line in enumerate(self.content):
            # Line Number
            ln_widget = QWidget()
            ln_widget.setStyleSheet("""
                background: #282c33;
                font-family: 'Lucida Console';
                font-size: 12px;
                border-right: 1px solid #8e8e8e;
                border-radius: 0;
            """ + """
                border-bottom-left-radius: 6px;
            """ * (n == len(self.content) - 1))
            ln_widget.setFixedWidth(mw)

            ln_layout = QVBoxLayout(ln_widget)
            ln_layout.setContentsMargins(4, 0, 0, 0)
            ln_layout.setSpacing(0)

            ln_label = QLabel(text=f"{n + 1}")
            ln_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
            ln_label.setStyleSheet("""
                color: #8e8e8e;
                padding-right: 4px;
            """)
            ln_layout.addWidget(ln_label)

            self.numbers.append(ln_widget)
            self.layout.addWidget(ln_widget, n, 0)

            # content
            self.lines.append(EditorLine(line))
            self.layout.addWidget(self.lines[-1], n, 1)

        self.layout.setRowStretch(len(self.content) - 1, 1)
        self.layout.setColumnStretch(1, 1)

    def load(self, path):
        with open(path, encoding='u16') as document:
            for i in range(len(self.lines)):
                self.layout.setRowStretch(i, 0)
                self.layout.removeWidget(self.numbers[i])
                self.layout.removeWidget(self.lines[i])
                self.lines[i].setParent(None)

            mw = 50
            self.numbers = []
            self.lines = []

            content = document.read().splitlines()

            for n, line in enumerate(content):
                # Line Number
                ln_widget = QWidget()
                ln_widget.setStyleSheet("""
                            background: #282c33;
                            font-family: 'Lucida Console';
                            font-size: 12px;
                            border-right: 1px solid #8e8e8e;
                            border-radius: 0;
                        """ + """
                            border-bottom-left-radius: 6px;
                        """ * (n == len(content) - 1))
                ln_widget.setFixedWidth(mw)

                ln_layout = QVBoxLayout(ln_widget)
                ln_layout.setContentsMargins(4, 0, 0, 0)
                ln_layout.setSpacing(0)

                ln_label = QLabel(text=f"{n + 1}")
                ln_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
                ln_label.setStyleSheet("""
                            color: #8e8e8e;
                            padding-right: 4px;
                        """)
                ln_layout.addWidget(ln_label)

                self.numbers.append(ln_widget)
                self.layout.addWidget(ln_widget, n, 0)

                # content
                self.lines.append(EditorLine(line))
                self.layout.addWidget(self.lines[-1], n, 1)

            self.layout.setRowStretch(len(content) - 1, 1)
