from PySide6.QtCore import Qt, QEvent
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
    class EnhancedLabel(QWidget):
        def __init__(self, content, pair, a_or_b):
            self.hover = False
            self.pair = pair
            super().__init__()

            self.installEventFilter(self)

            layout = QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            for s in content:
                w = None
                if type(s) is str: w = QLabel(text=s.strip())
                else: w = s.a() if a_or_b == 0 else s.b()
                layout.addWidget(w)
            self.hover_end()

        def eventFilter(self, watched, event):
            if event.type() == QEvent.Enter:
                super().enterEvent(event)
                self.hover = True
                if self.pair: self.pair.notify_hover(True)
                else: self.hover_start()
            elif event.type() == QEvent.Leave:
                super().leaveEvent(event)
                self.hover = False
                if self.pair: self.pair.notify_hover(False)
                else: self.hover_end()
            elif event.type() == QEvent.MouseButtonRelease:
                pass    # no click event currently
            return False

        def hover_start(self):
            bg = 'transparent'
            bd = '#525252'
            tx = 'white'
            if not self.pair:
                bg = 'rgba(140, 140, 140, 0.35)'
                bd = 'rgba(140, 140, 140, 0.8)'
            elif self.pair.error > 0:
                bg = ['', 'rgba(70, 140, 0, 0.35)', 'rgba(140, 0, 0, 0.35)'][self.pair.error]
                bd = ['', 'rgba(70, 140, 0, 1)', 'rgba(140, 0, 0, 1)'][self.pair.error]
            elif '?' in self.pair.flags:
                bg = 'rgba(140, 140, 0, 0.35)'
                bd = 'rgba(140, 140, 0, 1)'
            elif self.pair.sel_a and self.pair.sel_b:
                bg = 'rgba(0, 140, 0, 0.35)'
                bd = 'rgba(0, 140, 0, 1)'
            elif self.pair.sel_a or self.pair.sel_b:
                bg = 'rgba(15, 120, 200, 0.35)'
                bd = 'rgba(15, 120, 200, 1)'

            self.setStyleSheet(f'''
                background: {bg};
                color: {tx};
                border-radius: 2px;
                padding: 1px 0 0 0;
                border: 1px solid {bd};
            ''')

        def hover_end(self):
            bg = 'transparent'
            bd = '#525252'
            tx = '#aeaeae'

            if self.pair.error > 0:
                bg = ['', 'rgba(70, 140, 0, 0.08)', 'rgba(140, 0, 0, 0.08)'][self.pair.error]
                bd = ['', 'rgba(70, 140, 0, 0.3)', 'rgba(140, 0, 0, 0.3)'][self.pair.error]
            elif '?' in self.pair.flags:
                bg = 'rgba(140, 140, 0, 0.08)'
                bd = 'rgba(140, 140, 0, 0.3)'
            elif self.pair.sel_a and self.pair.sel_b:
                bg = 'rgba(0, 140, 0, 0.08)'
                bd = 'rgba(0, 140, 0, 0.3)'
            elif self.pair.sel_a or self.pair.sel_b:
                bg = 'rgba(15, 120, 200, 0.08)'
                bd = 'rgba(15, 120, 200, 0.3)'

            self.setStyleSheet(f'''
                background: {bg};
                color: {tx};
                border-radius: 2px;
                padding: 1px 0 0 0;
                border: 1px solid {bd};
            ''')

    class SelectionPair:
        def __init__(self, l_id, a=None, b=None, sel_pool=None, desc='No desc. found'):
            self.link_id = l_id
            self.sel_a = a
            self.sel_b = b
            self.la = None
            self.lb = None
            self.selection_pool = sel_pool
            self.description = desc
            self.error = 0
            self.flags = ''

        def a(self, nested=False):
            self.la = self._sp_label(self.sel_a, 0)
            return self.la

        def b(self, nested=False):
            self.lb = self._sp_label(self.sel_b, 1)
            return self.lb

        def _sp_label(self, content, a_or_b) -> QWidget:
            if content is None: return QLabel()

            label = EnhancedEditorLine.EnhancedLabel(content, self, a_or_b)
            label.setFixedHeight(16)
            label.setStyleSheet("""
                background: transparent;
                color: #aeaeae;
                border-radius: 2px;
                padding: 1px 0 0 0;
                border: 1px solid #525252;
            """)

            label.hover_end()
            return label

        def notify_hover(self, on_off: bool):
            if on_off:
                if self.la: self.la.hover_start()
                if self.lb: self.lb.hover_start()
            else:
                if self.la: self.la.hover_end()
                if self.lb: self.lb.hover_end()

    def __init__(self, lang_a, lang_b):
        super().__init__()
        # keeping unaltered versions of the two lines
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
            processed = ['']
            for s in contents:
                if type(s) is str:
                    if s.isnumeric():
                        if link_id < 0: link_id = int(s)
                        else: err = max(err, 1)
                    elif s in '_^?~': flags += s
                    else:
                        if type(processed[-1]) is not str: processed.append('')
                        processed[-1] += s
                else:   # s is a Selection Pair
                    processed.append(s)
            while '' in processed: processed.remove('')

            if link_id > 0 and link_id in pool:
                pair = pool[link_id]
                # a_or_b: a <- 0 | else -> b
                if a_or_b == 0:
                    if pair.sel_a: pair.error = max([pair.error, err, 1])
                    pair.sel_a = processed
                else:
                    if pair.sel_b: pair.error = max([pair.error, err, 1])
                    pair.sel_b = processed
                for f in flags:
                    if f not in pair.flags: pair.flags += f
                return pair
            else:
                while link_id <= 0 and link_id in pool: link_id -= 1
                pair = pool[link_id] = EnhancedEditorLine.SelectionPair(
                    link_id,
                    a=processed if a_or_b == 0 else None,
                    b=processed if a_or_b != 0 else None,
                    sel_pool=pool
                )
                for f in flags:
                    if f not in pair.flags: pair.flags += f

                return pair

        def split_line(line, a_or_b, pool):
            split = ['']
            for c in line:
                if c == ']' and '[' in split:
                    p = -split[::-1].index('[')
                    split, ctnt = split[:p-1], split[p:]
                    split.append(process(ctnt, pool, a_or_b))
                    split[-1].notify_hover(False)
                elif c in ' .,/;"[]-_~^?!':
                    split.extend([c, ''])
                else: split[-1] += c
            while '' in split: split.remove('')

            label_line = QWidget()
            label_line.setFixedHeight(19)
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
