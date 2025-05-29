from typing import List, Tuple
from models.process import Process

class SRT:
    @staticmethod
    def schedule(processes: List[Process]) -> List[Tuple[str, int, int]]:
        if not processes:
            return []
        
        schedule = []
        current_time = 0
        remaining_processes = processes.copy()
        current_process = None
        
        for p in remaining_processes:
            p.remaining_time = p.burst_time
        
        while remaining_processes:
            available = [p for p in remaining_processes if p.arrival_time <= current_time]
            
            if not available:
                current_time = min(p.arrival_time for p in remaining_processes)
                continue
            
            selected = min(available, key=lambda p: p.remaining_time)
            
            if current_process and current_process != selected:
                schedule.append((current_process.pid, current_process.start_time, current_time))
            
            if current_process != selected:
                selected.start_time = current_time
                current_process = selected
            
            next_arrival = float('inf')
            for p in remaining_processes:
                if p.arrival_time > current_time:
                    next_arrival = min(next_arrival, p.arrival_time)
            
            completion_time = current_time + selected.remaining_time
            next_event = min(next_arrival, completion_time)
            
            time_executed = next_event - current_time
            selected.remaining_time -= time_executed
            current_time = next_event
            
            if selected.remaining_time == 0:
                selected.completion_time = current_time
                selected.calculate_metrics()
                schedule.append((selected.pid, selected.start_time, current_time))
                remaining_processes.remove(selected)
                current_process = None
        
        return schedule

