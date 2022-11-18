from Section import Section


class Project:

    def __init__(self, name: str = "", sections: list = [], dictionary: dict = {}):
        self.name = name
        self.sections = sections
        self.dictionary = dictionary
