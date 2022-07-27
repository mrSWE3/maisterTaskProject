
import requests
from projectBuilder import ProjectBuilder
from ConsoleView import show
import asyncio
import nest_asyncio
import Irequest


class PydineRequest:
    def __init__(self) -> None:
        pass

    async def get(self, url: str, headers: dict) -> str:
        response = requests.request(
            url=url, headers=headers, method="GET").json()
        return response


async def program(token, name):
    pb = await ProjectBuilder.create(token=token, projectName=name, requestMaker=PydineRequest())

    while True:
        a, b, c = await pb.getInfoAsync()
        project = pb.build1(a, b, c)
        show(p=project)
        for i in range(3):
            print("----------")


if __name__ == '__main__':
    name = "Programmering"
    token = "EAt5sK7OxUh_pZWB2khILpK0KY1C7O_46XnddjmoYQM"

    asyncio.run(program(token=token, name=name))
