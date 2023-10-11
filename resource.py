from abc import ABC


class Resource(ABC):
    max_speed = 0

    def __init__(self, number: int | str):
        self.name = str(number)
        self.cur_speed = 0


class Tipper(Resource):
    max_speed = 80


class Excavator(Resource):
    max_speed = 40

    def __init__(self, number: int):
        self._name = ""
        super().__init__(number=number)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str | int):
        self._name = "Э" + str(name)


if __name__ == "__main__":
    a = Tipper(number=101)
    b = Excavator(number=102)
    print(a.name)
    print(b.name)
