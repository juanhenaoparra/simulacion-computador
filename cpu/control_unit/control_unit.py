from enum import Enum
import time
from cpu.models.instruction import Instruction
from cpu.control_unit.pc import ProgramCounter
from cpu.bus.bus import Bus, BusType, Commands
from cpu.memory.memory import MemoryType
from cpu.control_unit.mar import MemoryAddressRegister
from cpu.control_unit.mbr import MemoryBufferRegister, MBRNoneValueException
from cpu.models.events import EventBus, ResourceChange, ResourceType
from cpu.models.instruction import OperandDirection, InstructionHandler

OPERANDS_DIRECTIONS_MAP = {
    OperandDirection.IMMEDIATE: None,
    OperandDirection.REGISTER: MemoryType.REGISTER,
    OperandDirection.DIRECT: MemoryType.DATA,
}


class ControlUnitMode(str, Enum):
    STEP = "step"
    RUN = "run"


class ControlUnit:
    program_counter: ProgramCounter
    ir: Instruction
    bus_control: Bus
    mar: MemoryAddressRegister
    mbr: MemoryBufferRegister

    def __init__(self):
        self.running = True
        self.notify("program_started", None)
        self.program_counter = ProgramCounter()
        self.bus_control = Bus(
            BusType.CONTROL,
            lambda change: change.event == f"response_{BusType.CONTROL.value}",
        )
        self.mar = MemoryAddressRegister()
        self.mbr = MemoryBufferRegister()

    def run(self, mode: ControlUnitMode = ControlUnitMode.STEP, delay: int = 0.5):
        try:
            if mode == ControlUnitMode.STEP:
                self.execute_instruction()
            else:
                while self.running:
                    self.execute_instruction()

                    if delay > 0:
                        time.sleep(delay)

        except MBRNoneValueException:
            self.notify(
                "program_finished",
                {"position": self.program_counter.get_position_direction()},
            )

            EventBus.reset_listeners()
    def reset(self):
        self.running = True
        self.notify("program_started", None)
        self.program_counter = ProgramCounter()
        self.bus_control = Bus(
            BusType.CONTROL,
            lambda change: change.event == f"response_{BusType.CONTROL.value}",
        )
        self.mar = MemoryAddressRegister()
        self.mbr = MemoryBufferRegister()

    def execute_instruction(self):
        self.notify("fetch_instruction_started", None)
        self.fetch_instruction()
        self.decode_instruction()
        self.fetch_operands()
        self.execute()
        self.notify("fetch_instruction_finished", None)

    def fetch_instruction(self):
        instruction_position = self.program_counter.get_position_direction()

        self.bus_control.send(
            "send_command",
            command=Commands.OPEN_PROGRAM_MEMORY,
        )

        self.bus_control.send(
            "send_command",
            command=Commands.FETCH_VALUE,
            type=MemoryType.PROGRAM,
            address=instruction_position,
        )

        self.program_counter.increment()

    def decode_instruction(self):
        self.ir = Instruction(self.mbr.get_value())
        return self.ir

    def fetch_operands(self):
        for operand in self.ir.operands:
            memory_type = OPERANDS_DIRECTIONS_MAP[operand.direction]
            operand.set_memory_type(memory_type)

            if memory_type is None:
                operand.cache_value(operand.value)
                continue

            self.bus_control.send(
                "send_command",
                command=Commands.FETCH_VALUE,
                type=memory_type,
                address=operand.value,
            )

            try:
                operand.cache_value(self.mbr.get_value())
            except Exception:
                operand.cache_value(None)

    def execute(self):
        print(f"--> starting execution of instruction: {self.ir.codop}")
        result = InstructionHandler.exec(self.ir)
        print(f"--> instruction: {self.ir.codop}\n\tresult: {result}")

    def stop(self):
        self.running = False

    def notify(self, event: str, metadata: dict):
        EventBus.notify(ResourceChange(ResourceType.CU, event, metadata))

    def fetch_operand(self, memory_type: MemoryType, address: int):
        self.bus_control.send(
            "send_command",
            command=Commands.FETCH_VALUE,
            type=memory_type,
            address=address,
        )
