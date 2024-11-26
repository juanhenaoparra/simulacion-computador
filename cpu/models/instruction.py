from enum import Enum
from typing import List

from cpu.models.events import ResourceChange, ResourceType, EventBus
from cpu.models.directions import binary_to_number

INSTRUCTION_SIZE = 64
CODOP_SIZE = 4
OPERAND_DIRECTION_SIZE = 2
OPERAND_SIZE = 28


class CodOp(str, Enum):
    ADD = "0000"
    SUB = "0001"
    MUL = "0010"
    DIV = "0011"
    MOVE = "0100"
    SAVE = "0101"
    LOAD = "0110"
    JUMP = "0111"


class OperandDirection(str, Enum):
    IMMEDIATE = "00"
    REGISTER = "01"
    DIRECT = "10"


class Operand:
    value: str
    direction: OperandDirection
    cache: str

    def __init__(self, value: str, direction: str):
        self.value = value

        if direction not in OperandDirection.__members__.values():
            raise ValueError(f"La dirección del operando {direction} no es válida")

        self.direction = OperandDirection(direction)

    def get_cached_value(self):
        return self.cache

    def cache_value(self, v):
        self.cache = v


class Instruction:
    codop: CodOp
    operands: List[Operand]

    def __init__(self, instruction: str):
        self.validate_instruction(instruction)

        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.IR,
                event="current_instruction",
                metadata={
                    "codop": self.codop,
                    "operands": self.operands,
                },
            )
        )

    def validate_instruction(self, instruction: str):
        if len(instruction) != INSTRUCTION_SIZE:
            raise ValueError(
                f"La instrucción debe tener {INSTRUCTION_SIZE} bits. Tiene {len(instruction)} bits"
            )

        self.codop = CodOp(instruction[:CODOP_SIZE])

        if self.codop not in CodOp.__members__.values():
            raise ValueError(f"El código de operación {self.codop} no es válido")

        self.operands = []

        for i in range(
            CODOP_SIZE, INSTRUCTION_SIZE, OPERAND_SIZE + OPERAND_DIRECTION_SIZE
        ):
            operand_direction = instruction[i : i + OPERAND_DIRECTION_SIZE]
            operand_value = instruction[
                i + OPERAND_DIRECTION_SIZE : i + OPERAND_SIZE + OPERAND_DIRECTION_SIZE
            ]

            self.operands.append(
                Operand(value=operand_value, direction=operand_direction)
            )


class InstructionNotImplemented(Exception):
    pass


class InstructionHandler:
    @classmethod
    def handle_add(cls, instruction: Instruction):
        numbers = []
        # TODO: Implementar ALU
        print("Adding instruction: ", instruction)

        for operand in instruction.operands:
            numbers.append(binary_to_number(operand.get_cached_value()))

        return sum(numbers)

    @classmethod
    def handle_move(cls, instruction: Instruction):
        print("Moving instruction: ", instruction)

    @classmethod
    def exec(cls, instruction: Instruction):
        if instruction.codop == CodOp.ADD:
            return cls.handle_add(instruction)
        elif instruction.codop == CodOp.MOVE:
            return cls.handle_move(instruction)
        else:
            raise InstructionNotImplemented(
                f"La instrucción {instruction.codop} no ha sido implementada"
            )
