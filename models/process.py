from dataclasses import dataclass
from typing import Optional

@dataclass
class Process:
    pid: str
    burst_time: int
    arrival_time: int
    priority: int
    remaining_time: Optional[int] = None
    start_time: Optional[int] = None
    completion_time: Optional[int] = None
    waiting_time: Optional[int] = None
    turnaround_time: Optional[int] = None
    
    def __post_init__(self):
        if self.remaining_time is None:
            self.remaining_time = self.burst_time
    
    def calculate_metrics(self):
        if self.completion_time is not None and self.start_time is not None:
            self.turnaround_time = self.completion_time - self.arrival_time
            self.waiting_time = self.turnaround_time - self.burst_time

