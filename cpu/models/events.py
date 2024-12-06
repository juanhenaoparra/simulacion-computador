from enum import Enum
from dataclasses import dataclass
from typing import List, Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError


class ResourceType(str, Enum):
    IR = "ir"
    BUS = "bus"
    MAR = "mar"
    MBR = "mbr"
    PC = "pc"
    CU = "cu"
    ALU = "alu"
    INT = "int"


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
    _debug = False

    @classmethod
    def set_debug(cls, debug: bool) -> None:
        cls._debug = debug

    @classmethod
    def reset_listeners(cls) -> None:
        cls._listeners = {resource_type: [] for resource_type in ResourceType}

    @classmethod
    def subscribe(
        cls, resource_type: ResourceType, listener: Callable, filter: Callable = None
    ) -> None:
        subscription = {"listener": listener, "filter": filter}
        if subscription not in cls._listeners[resource_type]:
            cls._listeners[resource_type].append(subscription)

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
            future = cls._executor.submit(
                filter_change, listener["filter"], listener["listener"], change
            )
            futures.append(future)

        for future in futures:
            try:
                future.result(timeout=1.5)  
            except TimeoutError:
                print(f"Task: {future} took too long...")
                future.cancel()


def filter_change(filterFn: Callable, listenerFn: Callable, change: ResourceChange):
    if filterFn is None or filterFn(change):
        listenerFn(change)
