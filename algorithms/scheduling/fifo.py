from typing import List, Tuple
from models.process import Process

class FIFO:
    @staticmethod
    def schedule(processes: List[Process]) -> List[Tuple[str, int, int]]:
        if not processes:
            return []
        
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        schedule = []
        current_time = 0
        
        for process in sorted_processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            start_time = current_time
            end_time = current_time + process.burst_time
            
            process.start_time = start_time
            process.completion_time = end_time
            process.calculate_metrics()
            
            schedule.append((process.pid, start_time, end_time))
            current_time = end_time
        
        return schedule

