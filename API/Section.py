from Task import Task
class Section:
    def __init__(self, name:str = "", tasks: list[Task] = [],dictionary: dict = {}):
        self.name = name
        self.tasks = tasks
        self.dictionary = dictionary