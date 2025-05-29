from dataclasses import dataclass
from typing import List

@dataclass
class Resource:
    name: str
    count: int
    available: int = None
    waiting_processes: List[str] = None
    
    def __post_init__(self):
        if self.available is None:
            self.available = self.count
        if self.waiting_processes is None:
            self.waiting_processes = []
    
    def acquire(self, process_id: str) -> bool:
        if self.available > 0:
            self.available -= 1
            return True
        else:
            if process_id not in self.waiting_processes:
                self.waiting_processes.append(process_id)
            return False
    
    def release(self, process_id: str) -> str:
        self.available += 1
        if self.waiting_processes:
            return self.waiting_processes.pop(0)
        return None

