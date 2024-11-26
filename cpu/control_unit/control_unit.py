from enum import Enum
import time
from cpu.models.instruction import Instruction
from cpu.control_unit.pc import ProgramCounter
from cpu.bus.bus import Bus, BusType, Commands
from cpu.memory.memory import MemoryType
from cpu.control_unit.mar import MemoryAddressRegister
from cpu.control_unit.mbr import MemoryBufferRegister, MBRNoneValueException
from cpu.models.events import EventBus, ResourceChange, ResourceType


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
        self.program_counter = ProgramCounter()
        self.bus_control = Bus(BusType.CONTROL)
        self.mar = MemoryAddressRegister()
        self.mbr = MemoryBufferRegister()

    def run(self, mode: ControlUnitMode = ControlUnitMode.STEP, delay: int = 1):
        try:
            if mode == ControlUnitMode.STEP:
                self.execute_instruction()
            else:
                while self.running:
                    self.execute_instruction()

                    if delay > 0:
                        time.sleep(delay)

        except MBRNoneValueException:
            EventBus.notify(
                ResourceChange(
                    ResourceType.CU,
                    "program_finished",
                    {"position": self.program_counter.get_position_direction()},
                ),
            )

            EventBus.reset_listeners()

    def execute_instruction(self):
        self.fetch_instruction()
        self.decode_instruction()
        self.fetch_operands()
        self.execute()

    def fetch_instruction(self):
        instruction_position = self.program_counter.get_position_direction()

        self.bus_control.send(Commands.OPEN_PROGRAM_MEMORY)

        self.mar.set_value(MemoryType.PROGRAM, instruction_position)
        self.mar.dispatch()

        self.program_counter.increment()

    def decode_instruction(self):
        self.ir = Instruction(self.mbr.get_value())
        return self.ir

    def fetch_operands(self):
        pass

    def execute(self):
        pass

    def stop(self):
        self.running = False
