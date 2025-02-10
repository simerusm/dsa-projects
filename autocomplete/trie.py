from typing import *

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
    
class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """
        Insert a word into the Trie, marks the end of the word via TrieNode attribute flag
        """
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def _dfs(self, node: Optional[TrieNode], curr_str: str, words_with_prefix_ref: List[str]) -> None:
        """
        Dfs helper to collect all words starting from the current node (end of the prefix)
        """
        if node.is_end_of_word:
            words_with_prefix_ref.append(curr_str)
        
        for char, child in node.children.items():
            self._dfs(child, curr_str + char, words_with_prefix_ref)
    
    def _search(self, string: str) -> TrieNode | None:
        """
        Search trie to see if the string exists, returns the final character TrieNode if it does, otherwise None
        """
        node = self.root

        for char in string:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """
        Return all words in the trie starting with the given prefix
        """
        node = self._search(prefix)
        if not node:
            return []
        
        words_with_prefix = []
        self._dfs(node, prefix, words_with_prefix)
        return words_with_prefix