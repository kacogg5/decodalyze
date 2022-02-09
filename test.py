import time

from models.Trie import Trie

start = time.time()

english = Trie()

english.load("./models/tries/english.txt")

end = time.time()
print("Time elapsed:", end - start)
print(english.sibling_pairs, "pairs")
