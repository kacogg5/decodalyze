from PySide6.QtCore import Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView, QHBoxLayout, QLabel, QGridLayout, QScrollArea

from widgets.documentEditor import DocumentEditor


class DocumentView(QWidget):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.code = ""
        self.path = ""
        self.content = []

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 6, 0, 6)
        self.layout.setSpacing(0)

        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(20)
        self.title_bar.setStyleSheet("""
            background: #282c33;
            color: #8e8e8e;
            font-family: 'Lucida Console';
            font-size: 12px;
            border-bottom: 1px solid #8e8e8e;
            border-radius: 0;
            
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        """)

        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_layout.setContentsMargins(0, 6, 0, 0)

        self.title = QLabel(text=self.name if self.name else "No File Selected")
        self.title.setStyleSheet("""
            padding: 0 6px 0 6px;
        """)
        self.title_layout.addWidget(self.title)
        self.title_layout.addStretch(1)

        self.layout.addWidget(self.title_bar)
        self.layout.setStretch(1, 1)

        # editor
        self.scroll_adaptor = QScrollArea()
        self.scroll_adaptor.setStyleSheet("""
            QScrollBar:vertical {
                width: 16px;
                padding: 4px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #282c34;
                min-height: 10px;
                border-radius: 4px;
            }

            QScrollBar::add-line:vertical {
                background: transparent;
                height: 15px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical {
                background: transparent;
                height: 9px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: transparent;
            }

            QScrollBar::add-page:vertical {
                background: transparent;
            }

            QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        self.editor = DocumentEditor()

        self.scroll_adaptor.setWidgetResizable(True)
        self.scroll_adaptor.setWidget(self.editor)
        self.layout.addWidget(self.scroll_adaptor)

    def load(self, code, name, path) -> None:
        self.code = code
        self.name = name
        self.path = path
        self.title.setText(f"<span style=\"color: #52565d;\">{code} - </span>{name}<span style=\"color: #52565d;\"> - {path}</span>")
        self.editor.load(path)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.editor.resize(event.size().width() - 16, event.size().height())
