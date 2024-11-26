from enum import Enum
from typing import Callable

from cpu.models.directions import binary_to_number
from cpu.models.events import EventBus, ResourceChange, ResourceType


class MemoryType(str, Enum):
    DATA = "DATA"
    PROGRAM = "PROGRAM"
    REGISTER = "REGISTER"


class Memory:
    def __init__(self, type: MemoryType, filter=None):
        self.type = type
        self.memory = {}

        if filter is None:
            self.subscribe(
                ResourceType.BUS,
                lambda change: change.event == f"fetch_{self.type.value}",
            )
        else:
            self.subscribe(ResourceType.BUS, filter)

    def subscribe(self, resource_type: ResourceType, filter: Callable = None):
        EventBus.subscribe(
            resource_type,
            self.receive,
            filter=filter,
        )

    def receive(self, change: ResourceChange):
        value = self.read(change.metadata["address"])

        EventBus.notify(
            ResourceChange(
                ResourceType.BUS,
                f"response_memory_{self.type.value}",
                {"value": value, "type": self.type},
            )
        )

    def read(self, direction: str):
        direction_number = binary_to_number(direction)
        return self.memory.get(direction_number)

    def write(self, direction: str, value: str):
        direction_number = binary_to_number(direction)
        self.memory[direction_number] = value
