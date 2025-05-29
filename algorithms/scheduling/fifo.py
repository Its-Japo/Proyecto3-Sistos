from typing import List, Tuple
from models.process import Process

class FIFO:
    @staticmethod
    def schedule(processes: List[Process]) -> List[Tuple[str, int, int]]:
        """
        Returns list of (process_id, start_time, end_time) tuples
        """
        if not processes:
            return []
        
        # Sort by arrival time
        sorted_processes = sorted(processes, key=lambda p: p.arrival_time)
        schedule = []
        current_time = 0
        
        for process in sorted_processes:
            # Wait for process to arrive
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

