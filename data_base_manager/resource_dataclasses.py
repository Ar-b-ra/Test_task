from dataclasses import dataclass


@dataclass
class TypeResource:
    name: str
    max_speed: int


@dataclass
class Resource:
    name: str
    current_speed: int
    resource_type: TypeResource

    @property
    def speed_exceed(self) -> int:
        return int((self.current_speed - self.resource_type.max_speed) / self.resource_type.max_speed * 100) \
            if self.current_speed > self.resource_type.max_speed else 0
