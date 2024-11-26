from enum import Enum
from dataclasses import dataclass
from typing import List, Callable


class ResourceType(str, Enum):
    IR = "ir"
    BUS = "bus"
    MAR = "mar"
    MEMORY_PROGRAM = "memory_program"
    MEMORY_DATA = "memory_data"


@dataclass
class ResourceChange:
    resource_type: ResourceType
    event: str
    metadata: dict = None


class EventBus:
    _listeners: dict[ResourceType, List[Callable]] = {
        resource_type: [] for resource_type in ResourceType
    }

    @classmethod
    def subscribe(cls, resource_type: ResourceType, listener: Callable) -> None:
        cls._listeners[resource_type].append(listener)

    @classmethod
    def notify(cls, change: ResourceChange) -> None:
        if cls._listeners.get(change.resource_type) is None:
            return

        for listener in cls._listeners[change.resource_type]:
            # print(f"-> Notifying change: {change.event} with {change.metadata}")
            listener(change)
