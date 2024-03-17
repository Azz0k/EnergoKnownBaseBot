import re


class TwoWayDict:
    def __init__(self):
        self.name_to_id = dict()
        self.id_to_name = dict()
        self.next_id = 0
        self.pattern = '[ _-]+'

    def split_string_and_add(self, element: str):
        for el in re.split(self.pattern, element):
            self.add_element(el)

    def replace_names_with_ids(self, element: str):
        result = [self.get_id_from_name(x) for x in re.split(self.pattern, element)]
        return '_'.join(result)

    def replace_ids_with_names(self, element: str):
        result = [self.get_name_from_id(x) for x in re.split(self.pattern, element)]
        return '_'.join(result)

    def add_element(self, element: str):
        if element in self.name_to_id:
            return
        self.name_to_id[element] = str(self.next_id)
        self.id_to_name[str(self.next_id)] = element
        self.next_id += 1

    def get_id_from_name(self, name: str):
        return self.name_to_id[name]

    def get_name_from_id(self, identifier: str):
        return self.id_to_name[identifier]
