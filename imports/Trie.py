import re
from typing import Any


class Trie:
    class Node:

        def __init__(self):
            self.__children = dict()
            self.__value = 0

        def has_child(self, el: str) -> bool:
            if el in self.__children:
                return True
            return False

        def get_child(self, el: str) -> str:
            return self.__children[el]

        def add_child(self, el: str) -> None:
            if not self.has_child(el):
                self.__children[el] = self.__class__()

        def set_end(self, i: int) -> None:
            self.__value = i

        def get_index(self) -> int:
            return self.__value

        def get_children(self) -> Any:
            return list(self.__children.keys())

    __pattern = '[ _-]+'

    def __init__(self):
        self.root = Trie.Node()

    def insert(self, element: str, index: int) -> None:
        """Insert an element to the trie"""
        node = self.root
        for el in re.split(self.__pattern, element):  # element.split(split):
            if node.has_child(el):
                pass
            else:
                node.add_child(el)
            node = node.get_child(el)
        node.set_end(index)

    def get_index(self, element: str) -> int:
        """Find an element in the trie"""
        node = self.root
        for el in re.split(self.__pattern, element):
            if node.has_child(el):
                node = node.get_child(el)
            else:
                return -1
        return node.get_index()

    def get_children(self, element: str) -> Any:
        """Get list of child nodes from current node"""
        node = self.root
        if element == '':
            return node.get_children()
        for el in re.split(self.__pattern, element):
            if node.has_child(el):
                node = node.get_child(el)
            else:
                return []
        return node.get_children()
