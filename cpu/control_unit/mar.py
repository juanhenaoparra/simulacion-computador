from cpu.memory.memory import MemoryType
from cpu.models.events import ResourceChange, ResourceType, EventBus
from cpu.bus.bus import Bus, BusType, Commands


class MemoryAddressRegister:
    bus_directions: Bus

    def __init__(self):
        self.bus_directions = Bus(
            BusType.DIRECTIONS,
            lambda _: False,  # avoid subscribing to all events
        )
        self.value = ""
        self.type = ""

    def set_value(self, type: MemoryType, value: str):
        self.value = value
        self.type = type

        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.MAR,
                event="set_value",
                metadata={"value": value, "type": type},
            )
        )

        self.bus_directions.send(
            f"fetch_{self.type.value}",
            command=Commands.FETCH_VALUE,
            address=self.value,
        )

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value
