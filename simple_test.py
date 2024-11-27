from cpu.control_unit.control_unit import ControlUnit, ControlUnitMode
from cpu.memory.register import Register
from cpu.memory.memory import Memory, MemoryType
from cpu.models.directions import number_to_binary
from cpu.models.events import EventBus
from cpu.models.instruction import OperandDirection, CodOp

###
# ADD R1, R2
# MOV [1], 2
# END
###


def main():
    mp = Memory(MemoryType.PROGRAM)
    mp.write(
        number_to_binary(0, 28),  # instruction at 0
        CodOp.MOVE.value,
        +OperandDirection.DIRECT.value
        + number_to_binary(1, 28)  # value available in memory in position 1
        + OperandDirection.REGISTER.value
        + number_to_binary(2, 28),  # value available in memory in position 2
    )
    mp.write(
        number_to_binary(1, 28),
        CodOp.ADD.value
        + OperandDirection.DIRECT.value
        + number_to_binary(3, 28)  # value available in memory in position 3
        + OperandDirection.DIRECT.value
        + number_to_binary(4, 28),  # value available in memory in position 4
    )

    md = Memory(MemoryType.DATA)
    md.write(number_to_binary(1, 28), number_to_binary(10, 64))
    md.write(number_to_binary(2, 28), number_to_binary(20, 64))
    md.write(number_to_binary(3, 28), number_to_binary(30, 64))
    md.write(number_to_binary(4, 28), number_to_binary(40, 64))

    mr = Register()
    mr.write(number_to_binary(1, 28), number_to_binary(100, 64))
    mr.write(number_to_binary(2, 28), number_to_binary(200, 64))

    EventBus.set_debug(True)

    control_unit = ControlUnit()
    print("Running...")
    control_unit.run(mode=ControlUnitMode.RUN, delay=2)


main()
