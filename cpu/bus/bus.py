from enum import Enum
from typing import Callable

from cpu.models.events import ResourceChange, ResourceType, EventBus


class BusType(str, Enum):
    CONTROL = "CONTROL"
    DATA = "DATA"
    DIRECTIONS = "DIRECTIONS"


class Commands(str, Enum):
    OPEN_PROGRAM_MEMORY = "open_program_memory"
    OPEN_DATA_MEMORY = "open_data_memory"
    FETCH_VALUE = "fetch_value"


class Bus:
    def __init__(self, type: BusType, filter: Callable = None):
        self.type = type
        self.response_queue = []
        EventBus.subscribe(ResourceType.BUS, self.receive, filter)

    def send(self, event: str, **kwargs):
        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.BUS,
                event=event,
                metadata={"type": self.type, **kwargs},
            )
        )

    def receive(self, change: ResourceChange):
        self.response_queue.append(change.metadata["value"])

    def dequeue(self):
        return self.response_queue.pop(0)
