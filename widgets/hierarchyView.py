from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView, QLabel, QHBoxLayout, QScrollArea

from widgets.hierarchyToolbar import HierarchyToolbar


class DocumentTreeItem(QWidget):
    def __init__(self, text, click=lambda: None):
        super().__init__()
        self.text = text
        self.on_click = click

        self.hover = False

        self.installEventFilter(self)

        self.setFixedSize(self.width(), 20)
        self.setStyleSheet(f'''
            background: transparent;
            color: #8e8e8e;
            margin: 0 6px 0 6px;
            border-radius: 3px;
        ''')

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Enter:
            self.hover = True
            self.setStyleSheet(f'''
                background: rgba(185, 190, 200, 0.2);
                color: #8e8e8e;
                margin: 0 6px 0 6px;
                border-radius: 3px;
            ''')
        elif event.type() == QEvent.Leave:
            self.hover = False
            self.setStyleSheet(f'''
                background: transparent;
                color: #8e8e8e;
                margin: 0 6px 0 6px;
                border-radius: 3px;
            ''')
        elif event.type() == QEvent.MouseButtonRelease:
            self.on_click()
        return False


class DocumentTreeHeader(DocumentTreeItem):
    def __init__(self, text, click=lambda: None):
        super().__init__(text, click)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.cat_code = QLabel(text=self.text)
        self.layout.addWidget(self.cat_code)


class DocumentTreeDoc(DocumentTreeItem):
    def __init__(self, code, name, path, click=lambda c, n, p: None):
        super().__init__(name, lambda: click(code, name, path))

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 0, 0, 0)

        self.cat_code = QLabel(text=self.text)
        self.layout.addWidget(self.cat_code)


class HierarchyView(QWidget):
    def __init__(self, docs: dict, load):
        super().__init__()
        self.docs = docs
        self.load_doc = load

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.setSpacing(6)

        # Function Bar
        self.function_bar = HierarchyToolbar()
        self.layout.addWidget(self.function_bar)

        # Hierarchy List
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

        self.hierarchy_list = QWidget()
        self.hierarchy_list.setFixedWidth(self.width() / 2)
        self.hl_layout = QVBoxLayout(self.hierarchy_list)
        self.hl_layout.setContentsMargins(0, 0, 0, 0)
        self.hl_layout.setSpacing(0)

        self.sections = {}
        self.items = {}
        for code, cat in self.docs.items():
            self.sections[code] = DocumentTreeHeader(code)
            self.hl_layout.addWidget(self.sections[code])

            for name, path in cat.items():
                self.items[name] = DocumentTreeDoc(code, name, path, self.load_doc)
                self.hl_layout.addWidget(self.items[name])

        self.scroll_adaptor.setWidgetResizable(True)
        self.scroll_adaptor.setWidget(self.hierarchy_list)
        self.layout.addWidget(self.scroll_adaptor)
