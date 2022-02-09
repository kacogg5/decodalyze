def calculate_similarity(a, b):
    key_positions = {
        'q': (-1, -4.75),
        'w': (-1, -3.75),
        'e': (-1, -2.75),
        'r': (-1, -1.75),
        't': (-1, -0.75),
        'y': (-1, 0.25),
        'u': (-1, 1.25),
        'i': (-1, 2.25),
        'o': (-1, 3.25),
        'p': (-1, 4.25),
        'a': (0, -4.5),
        's': (0, -3.5),
        'd': (0, -2.5),
        'f': (0, -1.5),
        'g': (0, -0.5),
        'h': (0, 0.5),
        'j': (0, 1.5),
        'k': (0, 2.5),
        'l': (0, 3.5),
        'z': (1, -4),
        'x': (1, -3),
        'c': (1, -2),
        'v': (1, -1),
        'b': (1, 0),
        'n': (1, 1),
        'm': (1, 2),
    }

    def keyboard_score(word):
        if len(word) == 0: return 0, 0, 0

        from fold_to_ascii import fold
        total = 1
        dx = dy = 0
        x, y = (0, 0)
        for c in fold(word):
            tx, ty = key_positions[c]
            dx += tx
            dy += ty
            total += ((tx - x) ** 2 + (ty - y) ** 2) ** 0.5
            x, y = tx, ty
        return total / len(word), dx / len(word), dy / len(word)

    total_a, ax, ay = keyboard_score(a)
    total_b, bx, by = keyboard_score(b)
    diff = ((total_a - total_b) ** 2 + (ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
    return diff


class Trie:
    class TrieNode:
        def __init__(self):
            self.stem = ''
            self.char = ''
            self.end = False
            self.frequency = 0
            self.parent = self
            self.branches = {}
            self.siblings = {}

    closest_pair = ''
    closest_pair_sim = 1000
    sibling_pairs = 0

    def __init__(self):
        self.current_word = ''
        self.root = self.current = self.TrieNode()

    def load(self, file_name):
        with open(file_name, 'r', encoding='u16', errors='ignore') as file:
            self.reset()
            for line in file.readlines():
                word, freq = line.split()
                for l in word + ' ': self.move(l, int(freq))
            file.close()

    def save(self, file_name):
        with open(file_name, 'w', encoding='u16', errors='ignore') as file:
            words = []
            que = [('', self.root)]

            while que:
                stem, curr = que.pop(0)
                if curr is not self.root and curr.end:
                    words += [f"{stem} {curr.frequency}"]
                else:
                    que += [(stem + c, br) for c, br in curr.branches.items()]

            file.write('\n'.join(words))
            file.close()

    def move(self, letter, freq=1):
        if self.current is self.root and letter == ' ': return
        if letter in "1234567890~`!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/": return

        self.current_word += letter
        if letter in self.current.branches.keys():
            self.current = self.current.branches[letter]
            self.current.frequency += freq
        elif letter == " ":
            self.current.end = True
            self.update_siblings(self.current_word.strip())
            self.current_word = ""
            self.current = self.root
        else:
            new_node = self.TrieNode()
            new_node.parent = self.current
            self.current.branches[letter] = new_node
            self.current = new_node
            self.current.frequency += freq

    def back(self):
        self.current.frequency -= 1
        if self.current.frequency:
            self.current = self.current.parent
        else:
            char = self.current.char
            self.current = self.current.parent
            del self.current.branches[char]

    def reset(self):
        self.current = self.root

    def get_suggestions(self, k=3):
        words = {}
        que = [(self.current_word, 0, self.current)]
        visited = []

        checked = 0
        while que and checked < 1000:
            stem, score, curr = que.pop(0)
            if stem not in visited:
                if curr.end: words[stem] = score
                visited += [stem]
                que += [(stem + c, score + 0.25 * calculate_similarity(stem, stem + c) / max(1, branch.frequency), branch)
                        for c, branch in curr.branches.items()]
                que += [(name, score + calculate_similarity(self.current_word, name) / max(1, sibling.frequency), sibling)
                        for name, (sim, sibling) in curr.siblings.items()]
                que += [(stem[:-1], score + calculate_similarity(self.current_word, stem[:-1]) / max(1, curr.parent.frequency), curr.parent)]
                checked += 1

        if checked >= 1000:
            print("Terminated by iterations")
        return {w: words[w] for w in sorted(words, key=words.get)[:k]}

    def update_siblings(self, to_find):
        pre = ""
        curr = self.root
        word = f' {to_find}'
        while word:
            c, *word = word
            for f, branch in curr.branches.items():
                for l in word:
                    if l not in branch.branches:
                        break
                    else:
                        branch = branch.branches[l]
                else:
                    if branch.end and branch is not self.current:
                        this_word = pre + f + ''.join(word)
                        self.link_siblings(self.current, to_find, branch, this_word)

                    for x, ending in branch.branches.items():
                        if ending.end and ending is not self.current:
                            this_word = pre + f + ''.join(word) + x
                            self.link_siblings(self.current, to_find, ending, this_word)

            for f, branch in curr.branches.items():
                for l in word[1:]:
                    if l not in branch.branches:
                        break
                    else:
                        branch = branch.branches[l]
                else:
                    if branch.end and branch is not self.current:
                        this_word = pre + f + ''.join(word[1:])
                        self.link_siblings(self.current, to_find, branch, this_word)

                    for x, ending in branch.branches.items():
                        if ending.end and ending is not self.current:
                            this_word = pre + f + ''.join(word[1:]) + x
                            self.link_siblings(self.current, to_find, ending, this_word)
            if c != " ":
                pre += c
                curr = curr.branches[c]

    def link_siblings(self, branch, branch_word, sibling, sibling_word):
        if sibling_word not in branch.siblings:
            sim = calculate_similarity(branch_word, sibling_word)
            branch.siblings[sibling_word] = (sim, sibling)
            sibling.siblings[branch_word] = (sim, branch)
            if sim < self.closest_pair_sim:
                self.closest_pair = f"{sibling_word} - {branch_word}"
                self.closest_pair_sim = sim
            self.sibling_pairs += 1

