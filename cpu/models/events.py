from enum import Enum
from dataclasses import dataclass
from typing import List, Callable
from concurrent.futures import ThreadPoolExecutor


class ResourceType(str, Enum):
    IR = "ir"
    BUS = "bus"
    MAR = "mar"
    MBR = "mbr"
    PC = "pc"
    CU = "cu"
    # MEMORY_PROGRAM = "memory_program"
    # MEMORY_DATA = "memory_data"


@dataclass
class ResourceChange:
    resource_type: ResourceType
    event: str
    metadata: dict = None


class EventBus:
    _listeners: dict[ResourceType, List[Callable]] = {
        resource_type: [] for resource_type in ResourceType
    }
    _executor = ThreadPoolExecutor(max_workers=10)
    _debug = True

    @classmethod
    def set_debug(cls, debug: bool) -> None:
        cls._debug = debug

    @classmethod
    def reset_listeners(cls) -> None:
        cls._listeners = {resource_type: [] for resource_type in ResourceType}

    @classmethod
    def subscribe(cls, resource_type: ResourceType, listener: Callable) -> None:
        cls._listeners[resource_type].append(listener)

    @classmethod
    def notify(cls, change: ResourceChange) -> None:
        if cls._debug:
            print(
                f"-> Notifying change from {change.resource_type}: {change.event} with {change.metadata}"
            )

        if cls._listeners.get(change.resource_type) is None:
            return

        futures = []

        for listener in cls._listeners[change.resource_type]:
            future = cls._executor.submit(listener, change)
            futures.append(future)

        for future in futures:
            future.result()
