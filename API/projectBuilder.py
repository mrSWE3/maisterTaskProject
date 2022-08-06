from re import S
from xmlrpc.client import boolean
from Project import Project
import datetime
from Task import Task, Label, statusOfName
from Section import Section
from Irequest import Irequest
import asyncio


class ProjectBuilder:
    async def create(token: str, requestMaker: Irequest):
        self = ProjectBuilder()
        self.lastRequests = datetime.datetime.now()
        self.token = token
        self.requestMaker = requestMaker
        return self

    async def makeRequest(self, api_url: str):
        # print("now")
        header = {'Authorization': 'Bearer ' + self.token}
        now = datetime.datetime.now()
        diff = (now - self.lastRequests).total_seconds()

        while(diff < 0.52):
            now = datetime.datetime.now()
            diff = (now - self.lastRequests).total_seconds()
        response = await self.requestMaker.get(api_url, header)
        self.lastRequests = datetime.datetime.now()
        return response

    async def getProjects(self):
        respons = await self.makeRequest("https://www.meistertask.com/api/projects")
        return respons

    async def getProjectWithIdentifier(self, identifier, identifierValue):
        respons = await self.getProjects()
        projectJson = {}
        found = False
        for i in respons:
            if (i[identifier] == identifierValue):
                projectJson = i
                found = True
                break
        return projectJson

    async def getSectionsFromProject(self, projectId: int) -> dict:
        return list((await self.makeRequest("https://www.meistertask.com/api/projects/" + str(projectId) + "/sections")))

    async def getTasksFromSection(self, sectionId: int):
        return await self.makeRequest("https://www.meistertask.com/api/sections/" + str(sectionId) + "/tasks")

    async def getTasksFromProject(self, projectId: int):
        return await self.makeRequest("https://www.meistertask.com/api/projects/" + str(projectId) + "/tasks")

    async def getLabelFromtask(self, taskId: int):
        labelsJson = await self.makeRequest(
            "https://www.meistertask.com/api/tasks/" + str(taskId) + "/task_labels")
        return labelsJson

    async def addLabelsForEachTask(self, tasks, projectLabels):
        for i in range(len(tasks)):
            taskLabels = (await self.getLabelFromtask(tasks[i]["id"]))
            tasks[i]["labels"] = []
            for l in taskLabels:
                id = l["label_id"]
                labelDict = {"name": projectLabels[id]["name"],
                             "color": projectLabels[id]["color"]}
                tasks[i]["labels"].append(labelDict)

    async def getUserFromid(self, userId):
        if(userId == None):
            return "None"
        return await self.makeRequest("https://www.meistertask.com/api/persons/" + str(userId))["firstname"]

    async def getUsersFromProject(self, projectId: int):
        return await self.makeRequest("https://www.meistertask.com/api/projects/" + str(projectId) + "/persons")

    async def getLabels(self, projectId: int):
        return await self.makeRequest("https://www.meistertask.com/api/projects/" + str(projectId) + "/labels")

    async def getInfoAsync(self, projectIdentifier, projectIdentifierValue, onlyActiveSections: bool = True, onlyActiveTask: bool = True):
        projectJson = await self.getProjectWithIdentifier(projectIdentifier, projectIdentifierValue)
        projectId = projectJson["id"]
        sectionsJson = await self.getSectionsFromProject(projectId)
        if(onlyActiveSections):
            sectionsJson = keepDictsWithValueOnKey(
                sectionsJson, "status", 1)

        usersJson = await self.getUsersFromProject(projectId)
        tasksJson = await self.getTasksFromProject(projectId)
        if(onlyActiveTask):
            tasksJson = keepDictsWithValueOnKey(tasksJson, "status", 1)

        projectLabelsJson = await self.getLabels(projectId)
        await self.addLabelsForEachTask(tasks=tasksJson, projectLabels=listDictToDict(ds=projectLabelsJson, key="id"))
        return (projectJson, sectionsJson, tasksJson, usersJson)

    def build1(self, projectJson, sectionsJson, tasksJson, usersJson) -> Project:
        groupedTasks = groupDictsByKey(ds=tasksJson, key="section_id")
        self.addSectionsWithNoTasks(
            sectionsJson=sectionsJson, groupedTasks=groupedTasks)
        sectionsJson = sortDicts(sectionsJson, "sequence")
        sections = []
        for s in sectionsJson:
            tasks = []
            for t in groupedTasks[s["id"]]:
                assignedTo = findDict(
                    ds=usersJson, key="id", value=t["assigned_to_id"])
                if assignedTo == {}:
                    assignedTo = "None"
                else:
                    assignedTo = assignedTo["firstname"]
                labels = []
                for l in t.get("labels", []):
                    labels.append(Label(name=l["name"], hexColor=l["color"]))
                tasks.append(Task(dictionary=t,
                                  name=t["name"],
                                  labels=labels,
                                  assignedTo=assignedTo,
                                  notes=t["notes"],
                                  status=t["status"]))
            sections.append(Section(dictionary=s, name=s["name"], tasks=tasks))

        return Project(dictionary=projectJson, name=projectJson["name"], sections=sections)

    async def addLabels(self, tasksJson):
        for t in tasksJson:
            t.update({"labels": []})
        labelsJson = await self.getLabels()
        for l in labelsJson:

            ltasks = await self.makeRequest(
                "http://www.meistertask.com/api/tasks?labels=" + str(l["id"])+"/")
            for tl in ltasks:
                for t in tasksJson:
                    if t["id"] == tl["id"]:
                        t["labels"].append(l)
                        break

    def addSectionsWithNoTasks(self, sectionsJson, groupedTasks):
        for s in sectionsJson:
            hasTask = False
            for k in groupedTasks.keys():
                if k == s["id"]:
                    hasTask = True
                    break
            if not hasTask:
                groupedTasks.update({s["id"]: []})


def groupDictsByKey(ds: list[dict], key) -> dict:
    out = {}
    for d in ds:
        out.update({d[key]: []})
    for d in ds:
        out[d[key]].append(d)
    return out


def listDictToDict(ds: list[dict], key) -> dict:
    d = groupDictsByKey(ds, key)
    for key in d.keys():
        d[key] = d[key][0]
    return d


def filterDicts(ds: list[dict], key, value) -> list[dict]:
    out = []
    for d in ds:
        if d[key] == value:
            out.append(d)
    return out


def findDict(ds: list[dict], key, value) -> dict:
    for d in ds:
        if(d[key] == value):
            return d
    return {}


def keepDictsWithValueOnKey(ds: list[dict], key, value) -> list[dict]:
    out = []
    for d in ds:
        if d[key] == value:
            out.append(d)
    return out


def sortDicts(ds: list[dict], key) -> list[dict]:
    return sorted(ds, key=lambda x: x[key])
