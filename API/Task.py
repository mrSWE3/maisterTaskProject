#import CheckList
class Label:
    def __init__(self, name: str = "", hexColor: str = "000000"):
        self.name = name
        self.hexColor = hexColor

    def getColor(self) -> str:
        return "method not implemented"


class Task:
    def __init__(self, name: str = "",
                 labels: [Label] = [],
                 #checkList: list[CheckList] = "",
                 assignedTo: str = "",
                 notes: str = "",
                 status: int = 1,

                 dictionary: dict = {}
                 ):
        self.name = name
        self.labels = labels
        self.assignedTo = assignedTo
        self.notes = notes
        self.status = status
        self.dictionary = dictionary

    def nameOfStatus(self) -> str:
        if(self.status == 1):
            return "open"
        elif (self.status == 8):
            return "trashed"
        elif (self.status == 2):
            return "completed"
        elif (self.status == 18):
            return "completed_archived"
        else:
            return ""


def statusOfName(name: str) -> int:
    if(name == "open"):
        return 1
    elif (name == "trashed"):
        return 8
    elif (name == "completed"):
        return 2
    elif (name == "completed_archived"):
        return 18
    else:
        return ""
