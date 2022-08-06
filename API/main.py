
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
    pb = await ProjectBuilder.create(token=token, requestMaker=PydineRequest())

    while True:
        p, s, t, u = await pb.getInfoAsync("name", name)
        project = pb.build1(p, s, t, u)
        show(p=project)
        for i in range(3):
            print("----------")


if __name__ == '__main__':
    name = input("Name")
    token = input("token")
    asyncio.run(program(token=token, name=name))
