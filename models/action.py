from dataclasses import dataclass
from enum import Enum

class ActionType(Enum):
    READ = "READ"
    WRITE = "WRITE"

class ActionState(Enum):
    ACCESSED = "ACCEDIDO"
    WAITING = "ESPERANDO"

@dataclass
class Action:
    pid: str
    action_type: ActionType
    resource: str
    cycle: int
    state: ActionState = ActionState.WAITING

