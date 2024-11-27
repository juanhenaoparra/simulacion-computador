from enum import Enum
from typing import Callable

from cpu.models.directions import binary_to_number
from cpu.models.events import EventBus, ResourceChange, ResourceType
from cpu.bus.bus import Commands, BusType


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
                lambda change: change.metadata.get("type") == self.type
                and change.metadata.get("bus_type")
                == BusType.DIRECTIONS  # temporary to be able to fetch data when store
                and (
                    change.metadata.get("command") == Commands.FETCH_VALUE
                    or change.metadata.get("command") == Commands.STORE_VALUE
                ),
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
        if change.metadata.get("command") == Commands.FETCH_VALUE:
            value = self.read(change.metadata["address"])

            EventBus.notify(
                ResourceChange(
                    ResourceType.BUS,
                    f"response_memory_{self.type.value}",
                    {"value": value, "type": self.type},
                )
            )
        elif change.metadata.get("command") == Commands.STORE_VALUE:
            self.write(change.metadata["address"], change.metadata["value"])

            EventBus.notify(
                ResourceChange(
                    ResourceType.BUS,
                    f"write_memory_{self.type.value}",
                    {"value": change.metadata["value"], "type": self.type},
                )
            )

    def read(self, direction: str):
        direction_number = binary_to_number(direction)
        return self.memory.get(direction_number)

    def write(self, direction: str, value: str):
        direction_number = binary_to_number(direction)
        self.memory[direction_number] = value
