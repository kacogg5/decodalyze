import re

from models.Trie import Trie


def debracket(s: str) -> str:
    return re.sub(r"\[[^\]a-zA-Z]*([a-z][^\]]*[a-z])[^\]]*]", r"\1", s.lower())


with open("C:\\Users\\kacog\\OneDrive\\Documents\\Japanese Translations\\Phrases.txt", encoding="u8") as file:
    text = file.read().splitlines()

    romaji_trie = Trie()
    english_trie = Trie()

    curr_name = "Misc. Phrases"
    curr_code = "UDF"
    content = []

    count = 1
    for rl, el in zip(text[:-1], text[1:]):
        if rl.startswith("=="):
            # save current song
            name = re.sub(r"\W+", lambda x: x if str(x).isalpha() else "_", curr_name.lower())
            path = f"./docs/{name}.txt"
            with open(path, "w", encoding="u16", errors='ignore') as song_file:
                song_file.write("\n".join(content).strip())
            with open("./docs/inventory.txt", "r+") as inventory:
                temp = inventory.read().strip()
                inventory.write("\n" * (temp != "") + f"{curr_code}, {curr_name}, {path}")

            # reset for next song
            curr_code, *name = rl.strip(" []=").split(":")
            name = ":".join(name).strip()
            curr_name = name if name else f"Unnamed Song {count}"
            count += (not name)
            content = []
        elif any(c.isalpha()for c in rl) and any(c.isalpha()for c in el):
            romaji_trie.reset()
            for c in debracket(rl):
                romaji_trie.move(c)
            romaji_trie.move(" ")
            english_trie.reset()
            for c in debracket(el):
                english_trie.move(c)
            english_trie.move(" ")

            content.append(rl)
            content.append(el)
            content.append("")

    romaji_trie.save("./models/tries/romaji.txt")
    english_trie.save("./models/tries/english.txt")
