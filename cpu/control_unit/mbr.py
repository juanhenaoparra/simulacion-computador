from cpu.models.events import EventBus, ResourceChange, ResourceType


class MBRNoneValueException(Exception):
    pass


class MemoryBufferRegister:
    def __init__(self):
        self.type = ""
        self.value = ""

        EventBus.subscribe(ResourceType.BUS, self.set_value)

    def set_value(self, change: ResourceChange):
        if change.event.startswith("response_memory_"):
            self.value = change.metadata["value"]
            self.type = change.metadata["type"]

    def get_value(self):
        if self.value == "":
            raise Exception("memory buffer register is empty")

        if self.value is None:
            raise MBRNoneValueException("none value in memory buffer register")

        value = self.value
        self.value = ""
        return value
