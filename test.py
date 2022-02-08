import time

from models.Trie import Trie

start = time.time()

english = Trie()
# for c in "rough tough trough though thought through throughout" \
#          " thorough three them the then there that thorn thatch " \
#          "thistle thursday the":
#     english.move(c)
#     print(english.current_word+':', english.get_suggestions(3))

english.load("./models/tries/english.txt")

end = time.time()
print("Time elapsed:", end - start)
print(english.sibling_pairs, "pairs")
