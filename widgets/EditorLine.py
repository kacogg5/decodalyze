from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout


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
    class WordPair:
        def __init__(self, a=None, b=None, desc=None):
            self.word_a = a
            self.word_b = b
            self.description = desc

    def __init__(self, lang_a, lang_b):
        super().__init__()
        self.unedited_a = lang_a
        self.unedited_b = lang_b

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 0, 0, 1)
        self.layout.setSpacing(0)

        def split_line(line):
            split = [""]
            punctuation = ""
            for c in line:
                if c in ' .,/;"[]-_~!?':
                    split.append("")
                    punctuation += c
                else:
                    split[-1] += c

            label_line = QWidget()
            ll_layout = QHBoxLayout(label_line)
            ll_layout.setContentsMargins(0, 0, 0, 0)

            labels = []
            for word, p in zip(split, punctuation):
                word_label = QLabel(word)
                labels.append(word_label)
                ll_layout.addWidget(word_label)
                p_label = QLabel(p)
                labels.append(p_label)
                ll_layout.addWidget(p_label)

            return split, punctuation, label_line, ll_layout

        self.split_a, self.punct_a, self.line_a, self.la_layout = split_line(lang_a)
        self.layout.addWidget(self.line_a)
        self.split_b, self.punct_b, self.line_b, self.lb_layout = split_line(lang_b)
        self.layout.addWidget(self.line_b)
