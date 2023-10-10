class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end_of_word = True

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char.upper() in node.children:
                node = node.children[char.upper()]
            else:
                return []
        return self._get_words_from_node(node, prefix.upper())

    def _get_words_from_node(self, node, prefix):
        words = []
        if node.end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            words.extend(self._get_words_from_node(child_node, prefix + char))
        return words
