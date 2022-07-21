from cgitb import reset
from projectBuilder import ProjectBuilder
from ConsoleView import show
import asyncio
import nest_asyncio


def program(token, name):

    pb = ProjectBuilder(token=token, projectName=name)

    while True:
        project = pb.build1()
        show(p=project)
        for i in range(3):
            print("----------")


async def async1():
    await asyncio.sleep(1)
    print(sync())


def sync():
    result = asyncio.run(async2())
    result += ", was the return value"
    return result


async def async2():
    await asyncio.sleep(1)
    return "return value"

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(async1())
