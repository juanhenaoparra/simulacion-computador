from cpu.models.events import EventBus, ResourceChange, ResourceType


class MBRNoneValueException(Exception):
    pass


class MemoryBufferRegister:
    def __init__(self):
        self.response_queue = []

        EventBus.subscribe(
            ResourceType.BUS,
            self.set_value,
            lambda change: change.event.startswith("response_memory_"),
        )

    def set_value(self, change: ResourceChange):
        t = change.metadata["type"]
        value = change.metadata["value"]

        self.push_value(t, value)

        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.MBR,
                event="set_value",
                metadata={"value": value, "type": t},
            )
        )

    def push_value(self, type, value):
        self.response_queue.append({"type": type, "value": value})

    def get_value(self):
        try:
            first_element = self.response_queue.pop(0)
        except Exception:
            raise Exception("memory buffer register is empty")

        value = first_element.get("value")

        if value is None:
            raise MBRNoneValueException("none value in memory buffer register")

        return value
