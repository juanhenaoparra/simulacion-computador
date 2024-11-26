from cpu.models.events import EventBus, ResourceChange, ResourceType


class MBRNoneValueException(Exception):
    pass


class MemoryBufferRegister:
    def __init__(self):
        self.type = ""
        self.value = ""

        EventBus.subscribe(
            ResourceType.BUS,
            self.set_value,
            lambda change: change.event.startswith("response_memory_"),
        )

    def set_value(self, change: ResourceChange):
        self.value = change.metadata["value"]
        self.type = change.metadata["type"]

        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.MBR,
                event="set_value",
                metadata={"value": self.value, "type": self.type},
            )
        )

    def get_value(self):
        if self.value == "":
            raise Exception("memory buffer register is empty")

        if self.value is None:
            raise MBRNoneValueException("none value in memory buffer register")

        value = self.value
        self.value = ""
        return value
