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
    class SelectionPair:
        def __init__(self, l_id, a=None, b=None, sel_pool=None, desc='No desc. found'):
            self.link_id = l_id
            self.sel_a = list(a)
            self.sel_b = list(b)
            self.selection_pool = sel_pool
            self.description = desc
            self.error = 0
            self.flags = ''

        def a(self) -> QWidget:
            label = QWidget()
            layout = QHBoxLayout(label)
            for s in self.sel_a:
                if type(s) is str: layout.addWidget(QLabel(s))
                else:   # s is a nested SelectionPair
                    layout.addWidget(s.a())

            label.setFixedHeight(14)
            label.setStyleSheet("""
                border-radius: 2px;
                outline: 1px solid #525252;
            """)
            return label

        def b(self) -> QWidget:
            label = QWidget()
            layout = QHBoxLayout(label)
            for s in self.sel_b:
                if type(s) is str: layout.addWidget(QLabel(text=s))
                else:   # s is a nested SelectionPair
                    layout.addWidget(s.b())

            label.setStyleSheet("""
                border-radius: 2px;
                outline: 1px solid #525252;
            """)
            return label

    def __init__(self, lang_a, lang_b):
        super().__init__()
        # keeping an unaltered version of the line-pair
        self.unedited_a = lang_a
        self.unedited_b = lang_b
        self.pair_pool = {}

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 0, 0, 1)
        self.layout.setSpacing(0)

        # Creates Selection Pairs from an array of strings and
        # Selection Pairs
        def process(contents, pool, a_or_b):
            # a_or_b: a <- 0 | 1 -> b
            link_id = -1
            err = 0
            flags = ''
            processed = [""]
            pool: dict[int, EnhancedEditorLine.SelectionPair] = dict(pool)
            for s in contents:
                if type(s) is str:
                    if s.isnumeric():
                        if link_id < 0: link_id = int(s)
                        else: err = max(err, 1)
                    elif s in "_^?~": flags += s
                    else: processed[-1] += s
                else:   # s is a Selection Pair
                    processed.append(s)

            if link_id > 0 and link_id in pool:
                pair = pool[link_id]
                # a_or_b: a <- 0 | else -> b
                if a_or_b == 0:
                    if pair.sel_a is not None: pair.error = max([pair.error, err, 1])
                    pair.sel_a = processed
                else:
                    if pair.sel_b is not None: pair.error = max([pair.error, err, 1])
                    pair.sel_b = processed
            else:
                while link_id <= 0 and link_id in pool: link_id -= 1
                pool[link_id] = EnhancedEditorLine.SelectionPair(
                    link_id,
                    a=processed if a_or_b == 0 else None,
                    b=processed if a_or_b != 0 else None,
                    sel_pool=pool
                )

        def split_line(line, a_or_b, pool):
            split = [""]
            for c in line:
                if c == "]" and '[' in split:
                    p = split.rfind('[')
                    split, ctnt = split[:p], split[p:]
                    split.append(process(ctnt, pool, a_or_b))
                elif c in ' .,/;"[]-_~^?!': split.extend([c, ""])
                else: split[-1] += c

            label_line = QWidget()
            label_line.setFixedHeight(14)
            label_line.setStyleSheet("""
                background: transparent;
                color: #8e8e8e;
                font-family: 'Lucida Console';
                font-size: 12px;
                border-radius: 0;
            """)
            ll_layout = QHBoxLayout(label_line)
            ll_layout.setContentsMargins(2, 0, 0, 0)
            ll_layout.setSpacing(0)

            labels = []
            for word in split:
                if type(word) is str: labels.append(QLabel(text=word))
                else: labels.append(word.a() if a_or_b == 0 else word.b())
                ll_layout.addWidget(labels[-1])

            ll_layout.addStretch()
            return split, label_line, ll_layout

        self.split_a, self.line_a, self.la_layout = split_line(lang_a, 0, self.pair_pool)
        self.layout.addWidget(self.line_a)
        self.split_b, self.line_b, self.lb_layout = split_line(lang_b, 1, self.pair_pool)
        self.layout.addWidget(self.line_b)

        self.layout.addStretch()
