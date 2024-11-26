from cpu.models.directions import number_to_binary
from cpu.models.instruction import OPERAND_SIZE


class ProgramCounter:
    position: int
    position_direction: str

    def __init__(self):
        self.position = 0

    def increment(self):
        self.position += 1

    def get_position(self):
        return self.position

    def get_position_direction(self, size: int = OPERAND_SIZE):
        return number_to_binary(self.position, size)
