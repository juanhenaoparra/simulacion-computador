from cpu.memory.memory import MemoryType
from cpu.models.events import ResourceChange, ResourceType, EventBus


class MemoryAddressRegister:
    def __init__(self):
        self.value = ""
        self.type = ""

    def set_value(self, type: MemoryType, value: str):
        self.value = value
        self.type = type

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def dispatch(self):
        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.BUS,
                event=f"fetch_{self.type.value}",
                metadata={"address": self.value},
            )
        )
