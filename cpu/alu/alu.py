from cpu.models.directions import binary_to_number, number_to_binary, number_coma_flotante
from cpu.models.events import EventBus, ResourceChange, ResourceType
from cpu.models.constants import INSTRUCTION_SIZE


class ALU:
    @classmethod
    def add(cls, a: float, b: float):
        
        val = a + b
        val = number_coma_flotante(val)
        op1 = number_coma_flotante(a)
        op2 = number_coma_flotante(b)

        cls.notify(
            "alu_result",
            {
                "operation": "add",
                "operand_1":  op1,
                "operand_2": op2,
                "result": val,
            },
        )

        return val

    @classmethod
    def sub(cls, a: float, b: float):
        val = a - b
        val = number_coma_flotante(val)
        op1 = number_coma_flotante(a)
        op2 = number_coma_flotante(b)
        cls.notify(
            "alu_result",
            {"operation": "sub", "operand_1": op1, "operand_2": op2, "result": val},
        )

        return val

    @classmethod
    def mul(cls, a: float, b: float):
        val = a * b
        val = number_coma_flotante(val)
        op1 = number_coma_flotante(a)
        op2 = number_coma_flotante(b)

        cls.notify(
            "alu_result",
            {"operation": "mul", "operand_1": op1, "operand_2": op2, "result": val},
        )

        return val

    @classmethod
    def div(cls, a: float, b: float):
        val = a / b
        val = number_coma_flotante(val)
        op1 = number_coma_flotante(a)
        op2 = number_coma_flotante(b)

        cls.notify(
            "alu_result",
            {"operation": "div", "operand_1": op1, "operand_2": op2, "result": val},
        )

        return val
    @classmethod
    def comp(cls, a: float, b: float):
        val = a - b
        val = number_coma_flotante(val)
        op1 = number_coma_flotante(a)
        op2 = number_coma_flotante(b)

        cls.notify(
            "alu_result",
            {"operation": "sub", "operand_1": op1, "operand_2": op2, "result": val},
        )

        return val

    @classmethod
    def notify(cls, event: str, metadata: dict):
        EventBus.notify(ResourceChange(ResourceType.ALU, event, metadata))
