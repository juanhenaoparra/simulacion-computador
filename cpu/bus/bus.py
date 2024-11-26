from enum import Enum
from cpu.models.events import ResourceChange, ResourceType, EventBus


class BusType(str, Enum):
    CONTROL = "CONTROL"
    DATA = "DATA"
    DIRECTIONS = "DIRECTIONS"


class Commands(str, Enum):
    OPEN_PROGRAM_MEMORY = "open_program_memory"
    OPEN_DATA_MEMORY = "open_data_memory"


class Bus:
    def __init__(self, type: BusType):
        self.type = type
        self.response_queue = []
        EventBus.subscribe(ResourceType.BUS, self.receive)

    def send(self, command: str):
        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.BUS,
                event=f"send_{self.type.value}",
                metadata={"type": self.type, "command": command},
            )
        )

    def receive(self, change: ResourceChange):
        if change.event == f"response_{self.type.value}":
            self.response_queue.append(change.metadata["value"])

    def dequeue(self):
        return self.response_queue.pop(0)
