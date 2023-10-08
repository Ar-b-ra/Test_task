class SomeCar:
    max_speed = 0

    def __init__(self, number: int):
        self.name = str(number)
        self.cur_speed = 0


class Tipper(SomeCar):
    max_speed = 80


class Excavator(SomeCar):
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
