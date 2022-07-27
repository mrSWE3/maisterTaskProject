from Project import Project
import datetime
from Task import Task, Label, statusOfName
from Section import Section
from Irequest import Irequest
import asyncio


class ProjectBuilder:
    async def create(token: str, projectName: str, requestMaker: Irequest):
        self = ProjectBuilder()
        self.lastRequests = datetime.datetime.now()

        self.token = token
        self.projectName = projectName
        self.requestMaker = requestMaker
        respons = await self.makeRequest("https://www.meistertask.com/api/projects")
        projectJson = {}
        found = False
        for i in respons:
            if (i["name"] == projectName):
                projectJson = i
                found = True
                break
        if (not found):
            print("Can't find project")
        self.projectId = projectJson["id"]
        self.projectJson = projectJson
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

    async def getSectionsFromProject(self) -> dict:
        return list((await self.makeRequest("https://www.meistertask.com/api/projects/" + str(self.projectId) + "/sections")))

    async def getTasksFromSection(self, sectionId: int):
        return await self.makeRequest("https://www.meistertask.com/api/sections/" + str(sectionId) + "/tasks")

    async def getTasksFromProject(self):
        return await self.makeRequest("https://www.meistertask.com/api/projects/" + str(self.projectId) + "/tasks")

    async def getLabelFromtask(self, taskId: int):
        labelsJson = await self.makeRequest(
            "https://www.meistertask.com/api/tasks/" + str(taskId) + "/labels")
        labels = []
        for l in labelsJson:
            labels.append(l["name"])
        return labels

    async def getUserFromid(self, userId):
        if(userId == None):
            return "None"
        return await self.makeRequest("https://www.meistertask.com/api/persons/" + str(userId))["firstname"]

    async def getUsersFromProject(self):
        return await self.makeRequest("https://www.meistertask.com/api/projects/" + str(self.projectId) + "/persons")

    async def getLabels(self):
        return await self.makeRequest("https://www.meistertask.com/api/projects/" + str(self.projectId) + "/labels")

    async def getInfoAsync(self):
        sectionsJson = await self.getSectionsFromProject()
        usersJson = await self.getUsersFromProject()
        tasksJson = await self.getTasksFromProject()
        # await self.addLabels(tasksJson=tasksJson)
        return sectionsJson, tasksJson, usersJson

    def build1(self, sectionsJson, tasksJson, usersJson) -> Project:
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

        return Project(dictionary=self.projectJson, name=self.projectName, sections=sections)

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


def groupDictsByKey(ds: list[dict], key: str):
    out = {}
    for d in ds:
        out.update({d[key]: []})
    for d in ds:
        out[d[key]].append(d)
    return out


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


def sortDicts(ds: list[dict], key) -> list[dict]:
    return sorted(ds, key=lambda x: x[key])
