from typing import Any


class ContentsElement:
    def __init__(self, element_id: str, name: str, link: str = '', parent: Any = None):
        self.id = element_id
        self.name = name
        self.parent = parent
        self.link = link
        self.children = []

    def add_child(self,  element_id: str, name: str, link: str):
        child = ContentsElement(element_id, name, link, self)
        self.children.append(child)
