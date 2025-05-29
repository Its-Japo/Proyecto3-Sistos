from typing import List, Tuple
from models.process import Process
from collections import deque

class RoundRobin:
    @staticmethod
    def schedule(processes: List[Process], quantum: int = 2) -> List[Tuple[str, int, int]]:
        if not processes:
            raise ValueError("Process list cannot be empty")
        
        if quantum <= 0:
            raise ValueError(f"Quantum must be positive, got {quantum}")
        
        if quantum > 1000:  # Reasonable upper limit
            raise ValueError(f"Quantum too large: {quantum}")
        
        for i, process in enumerate(processes):
            if not hasattr(process, 'pid') or not process.pid:
                raise ValueError(f"Process {i}: Invalid or missing PID")
            
            if not hasattr(process, 'burst_time') or process.burst_time <= 0:
                raise ValueError(f"Process {process.pid}: Burst time must be positive")
            
            if not hasattr(process, 'arrival_time') or process.arrival_time < 0:
                raise ValueError(f"Process {process.pid}: Arrival time cannot be negative")
        
        pids = [p.pid for p in processes]
        if len(pids) != len(set(pids)):
            raise ValueError("Duplicate process IDs found")
        
        try:
            schedule = []
            current_time = 0
            ready_queue = deque()
            remaining_processes = sorted(processes, key=lambda p: p.arrival_time)
            
            # Reset remaining times
            for p in remaining_processes:
                p.remaining_time = p.burst_time
            
            process_index = 0
            max_iterations = len(processes) * 1000  
            iterations = 0
            
            while remaining_processes or ready_queue:
                iterations += 1
                if iterations > max_iterations:
                    raise RuntimeError("Algorithm exceeded maximum iterations (possible infinite loop)")
                
                while (process_index < len(remaining_processes) and 
                       remaining_processes[process_index].arrival_time <= current_time):
                    ready_queue.append(remaining_processes[process_index])
                    process_index += 1
                
                if not ready_queue:
                    if process_index < len(remaining_processes):
                        current_time = remaining_processes[process_index].arrival_time
                    continue
                
                current_process = ready_queue.popleft()
                
                execution_time = min(quantum, current_process.remaining_time)
                start_time = current_time
                end_time = current_time + execution_time
                
                if current_process.start_time is None:
                    current_process.start_time = start_time
                
                current_process.remaining_time -= execution_time
                current_time = end_time
                
                schedule.append((current_process.pid, start_time, end_time))
                
                while (process_index < len(remaining_processes) and 
                       remaining_processes[process_index].arrival_time <= current_time):
                    ready_queue.append(remaining_processes[process_index])
                    process_index += 1
                
                if current_process.remaining_time == 0:
                    current_process.completion_time = current_time
                    current_process.calculate_metrics()
                    remaining_processes.remove(current_process)
                else:
                    ready_queue.append(current_process)
            
            if not schedule:
                raise RuntimeError("Algorithm produced empty schedule")
            
            return schedule
            
        except Exception as e:
            if isinstance(e, (ValueError, RuntimeError)):
                raise
            else:
                raise RuntimeError(f"Unexpected error in Round Robin algorithm: {str(e)}")

