from cpu.models.directions import binary_to_number, number_to_binary
from cpu.models.instruction import INSTRUCTION_SIZE
from cpu.models.events import EventBus, ResourceChange, ResourceType


class ALU:
    @classmethod
    def add(cls, a: str, b: str):
        val = number_to_binary(
            binary_to_number(a) + binary_to_number(b), INSTRUCTION_SIZE
        )

        cls.notify(
            "alu_result",
            {
                "operation": "add",
                "operand_1": a,
                "operand_2": b,
                "result": val,
            },
        )

        return val

    @classmethod
    def sub(cls, a: str, b: str):
        val = number_to_binary(
            binary_to_number(a) - binary_to_number(b), INSTRUCTION_SIZE
        )

        cls.notify(
            "alu_result",
            {"operation": "sub", "operand_1": a, "operand_2": b, "result": val},
        )

        return val

    @classmethod
    def mul(cls, a: str, b: str):
        val = number_to_binary(
            binary_to_number(a) * binary_to_number(b), INSTRUCTION_SIZE
        )

        cls.notify(
            "alu_result",
            {"operation": "mul", "operand_1": a, "operand_2": b, "result": val},
        )

        return val

    @classmethod
    def div(cls, a: str, b: str):
        val = number_to_binary(
            binary_to_number(a) / binary_to_number(b), INSTRUCTION_SIZE
        )

        cls.notify(
            "alu_result",
            {"operation": "div", "operand_1": a, "operand_2": b, "result": val},
        )

        return val

    @classmethod
    def notify(cls, event: str, metadata: dict):
        EventBus.notify(ResourceChange(ResourceType.ALU, event, metadata))
