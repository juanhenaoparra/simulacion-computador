from cpu.models.directions import number_to_binary
from cpu.models.instruction import OPERAND_SIZE
from cpu.models.events import EventBus, ResourceChange, ResourceType


class ProgramCounter:
    position: int
    position_direction: str

    def __init__(self):
        self.position = 0
        self.notify_position_change()

    def increment(self):
        self.position += 1
        self.notify_position_change()

    def get_position(self):
        return self.position

    def get_position_direction(self, size: int = OPERAND_SIZE):
        return number_to_binary(self.position, size)

    def notify_position_change(self):
        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.PC,
                event="position_change",
                metadata={"position": self.position},
            )
        )
