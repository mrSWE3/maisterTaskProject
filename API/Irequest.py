from abc import abstractmethod


class Irequest:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get(url: str, headers: dict) -> str:
        pass
