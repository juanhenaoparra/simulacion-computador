from enum import Enum
from typing import List

from cpu.models.constants import (
    INSTRUCTION_SIZE,
    CODOP_SIZE,
    OPERAND_DIRECTION_SIZE,
    OPERAND_SIZE,
)
from cpu.models.events import ResourceChange, ResourceType, EventBus
from cpu.bus.bus import Commands, BusType
from cpu.memory.memory import MemoryType, Memory
from cpu.alu.alu import ALU
from cpu.models.directions import interpretar_flotante_a_decimal, binary_to_number


class CodOp(str, Enum):
    """
    Codigos de operación.
    1. Las operaciones aritméticas y lógicas son las únicas que pueden ser ejecutadas por la ALU.
      1. La ALU guardara en la dirección del primer operando el resultado de la operación. Sobreescribiendo su valor.
      2. Por ende el primer operando debe ser un registro o una posición de memoria.
    2. La instruccion MOVE copiara el valor del segundo operando en la dirección del primer operando.
      1. Por ende el primer operando debe ser un registro o una posición de memoria.
      2. Y el segundo operando puede ser un valor inmediato, un registro o una posición de memoria.
    """

    ADD = "0000"
    SUB = "0001"
    MUL = "0010"
    DIV = "0011"
    MOVE = "0100"
    SAVE = "0101"
    LOAD = "0110"
    JUMP = "0111"
    COMP = "1000"


class OperandDirection(str, Enum):
    IMMEDIATE = "00"
    REGISTER = "01"
    DIRECT = "10"


class Operand:
    value: str
    direction: OperandDirection
    memory_type: MemoryType
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

    def set_memory_type(self, memory_type: MemoryType):
        self.memory_type = memory_type

    def get_memory_type(self):
        return self.memory_type


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
    def handle_alu(cls, instruction: Instruction):
        if len(instruction.operands) != 2:
            raise ValueError("La instrucción aritmética debe tener dos operandos")

        if instruction.operands[0].direction == OperandDirection.IMMEDIATE:
            raise ValueError(
                "El primer operando de una instrucción aritmética no puede ser inmediato"
            )

        operand_1 = instruction.operands[0].get_cached_value()
        operand_2 = instruction.operands[1].get_cached_value()
        operand_1 = interpretar_flotante_a_decimal(operand_1)
        operand_2 = interpretar_flotante_a_decimal(operand_2)
        
        result = None

        if instruction.codop == CodOp.ADD: 
            result = ALU.add(operand_1, operand_2)
        elif instruction.codop == CodOp.SUB:
            result = ALU.sub(operand_1, operand_2)
        elif instruction.codop == CodOp.MUL:
            result = ALU.mul(operand_1, operand_2)
        elif instruction.codop == CodOp.DIV:
            result = ALU.div(operand_1, operand_2)
        elif instruction.codop == CodOp.COMP:
            result = ALU.comp(operand_1, operand_2)
        else:
            raise InstructionNotImplemented(
                f"La ALU no implementa la operación {instruction.codop}"
            )

        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.BUS,
                event="send_command",
                metadata={
                    "bus_type": BusType.DIRECTIONS,  # HACK: To be able to write it should travel through the data bus
                    "type": instruction.operands[0].get_memory_type(),
                    "command": Commands.STORE_VALUE,
                    "address": instruction.operands[0].value,
                    "value": result,
                },
            )
        )

        return result

    @classmethod
    def handle_move(cls, instruction: Instruction):
        if len(instruction.operands) != 2:
            raise ValueError("La instrucción MOVE debe tener dos operandos")

        if instruction.operands[0].direction == OperandDirection.IMMEDIATE:
            raise ValueError(
                "El primer operando de una instrucción MOVE no puede ser inmediato"
            )

        destination = instruction.operands[0].value
        destination_memory_type = instruction.operands[0].get_memory_type()
        source_value = instruction.operands[1].get_cached_value()

        EventBus.notify(
            ResourceChange(
                resource_type=ResourceType.BUS,
                event="send_command",
                metadata={
                    "bus_type": BusType.DIRECTIONS,  # HACK: To be able to write it should travel through the data bus
                    "type": destination_memory_type,
                    "command": Commands.STORE_VALUE,
                    "address": destination,
                    "value": source_value,
                },
            )
        )

        return source_value

    @classmethod
    def exec(cls, instruction: Instruction):
        if (
            instruction.codop == CodOp.ADD
            or instruction.codop == CodOp.SUB
            or instruction.codop == CodOp.MUL
            or instruction.codop == CodOp.DIV
        ):
            print("esta es la instruccion", instruction)
            return cls.handle_alu(instruction)
        elif instruction.codop == CodOp.MOVE:
            return cls.handle_move(instruction)
        else:
            raise InstructionNotImplemented(
                f"La instrucción {instruction.codop} no ha sido implementada"
            )
