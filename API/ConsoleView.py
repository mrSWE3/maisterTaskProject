
from Project import Project
from Task import Label


def show(p: Project):

    print("Project name:", p.name)
    sections = p.sections

    for s in sections:
        print("Section name:", s.name)
        for i in range(len(s.tasks)):
            task = s.tasks[i]
            labels = ""
            for l in task.labels:
                labels
            print("Task", str(i+1), "|", "name:", task.name, "|", "assignee:", task.assignedTo,
                  "|", "status:", task.nameOfStatus(), "|", "labels:", lineUpLabels(task.labels))


def lineUpLabels(labels: list[Label]):
    if (len(labels) < 1):
        return "None"
    s = labels[0].name
    for i in range(1, (len(labels))):
        s = s + ", " + labels[i].name
    return s
