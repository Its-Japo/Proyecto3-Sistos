from typing import List, Tuple
from models.process import Process

class SJF:
    @staticmethod
    def schedule(processes: List[Process]) -> List[Tuple[str, int, int]]:
        if not processes:
            return []
        
        schedule = []
        current_time = 0
        remaining_processes = processes.copy()
        
        while remaining_processes:
            available = [p for p in remaining_processes if p.arrival_time <= current_time]
            
            if not available:
                current_time = min(p.arrival_time for p in remaining_processes)
                continue
            
            selected = min(available, key=lambda p: p.burst_time)
            
            start_time = current_time
            end_time = current_time + selected.burst_time
            
            selected.start_time = start_time
            selected.completion_time = end_time
            selected.calculate_metrics()
            
            schedule.append((selected.pid, start_time, end_time))
            current_time = end_time
            remaining_processes.remove(selected)
        
        return schedule

