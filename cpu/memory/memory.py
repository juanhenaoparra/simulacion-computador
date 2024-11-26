from enum import Enum
from cpu.models.directions import binary_to_number
from cpu.models.events import EventBus, ResourceChange, ResourceType


class MemoryType(str, Enum):
    DATA = "DATA"
    PROGRAM = "PROGRAM"


class Memory:
    def __init__(self, type: MemoryType):
        self.type = type
        self.memory = {}

        EventBus.subscribe(ResourceType.BUS, self.receive)

    def receive(self, change: ResourceChange):
        if change.event == f"fetch_{self.type.value}":
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
