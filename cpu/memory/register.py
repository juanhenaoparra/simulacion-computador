from cpu.memory.memory import Memory, MemoryType
from cpu.bus.bus import Commands


class Register(Memory):
    def __init__(self):
        super().__init__(
            MemoryType.REGISTER,
            lambda change: (
                change.event == "send_command"
                and change.metadata.get("type") == MemoryType.REGISTER
                and (
                    change.metadata.get("command") == Commands.FETCH_VALUE
                    or change.metadata.get("command") == Commands.STORE_VALUE
                )
            ),
        )
