from dataclasses import dataclass


@dataclass
class TypeResource:
    """
    Структура типа ресурса.
    :param: name: имя типа ресурса
    :param: max_speed: максимальная скорость типа ресурса
    """
    name: str
    max_speed: int


@dataclass
class Resource:
    """
    Структура экземпляра ресурса.
    :param: name: имя ресурса
    :param: current_speed: текущая скорость типа ресурса
    :param: тип ресурсва, к которому принадлежит данный ресурс
    """
    name: str
    current_speed: int
    resource_type: TypeResource

    @property
    def speed_exceed(self) -> int:
        return int((self.current_speed - self.resource_type.max_speed) / self.resource_type.max_speed * 100) \
            if self.current_speed > self.resource_type.max_speed else 0
