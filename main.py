from cpu.control_unit.control_unit import ControlUnit, ControlUnitMode
from cpu.memory.memory import Memory, MemoryType
from cpu.models.directions import number_to_binary
from cpu.models.events import EventBus


def main():
    mp = Memory(MemoryType.PROGRAM)
    mp.write(
        number_to_binary(0, 28),  # instruction at 0
        "0100" + "00" + number_to_binary(1, 28) + "10" + number_to_binary(2, 28),
    )
    mp.write(
        number_to_binary(1, 28),
        "0000" + "00" + number_to_binary(3, 28) + "01" + number_to_binary(4, 28),
    )

    EventBus.set_debug(True)

    control_unit = ControlUnit()
    print("Running...")
    control_unit.run(mode=ControlUnitMode.RUN, delay=3)


if __name__ == "__main__":
    main()
