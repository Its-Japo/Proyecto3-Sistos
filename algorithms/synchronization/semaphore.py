from typing import List, Dict, Tuple
from models.process import Process
from models.resource import Resource
from models.action import Action, ActionState

class Semaphore:
    @staticmethod
    def simulate(processes: List[Process], resources: List[Resource], 
                actions: List[Action]) -> List[Tuple[str, str, int, int, ActionState]]:
        """
        Returns list of (process_id, action, start_time, end_time, state) tuples
        """
        if not actions:
            return []
        
        # Create resource map
        resource_map = {r.name: r for r in resources}
        
        # Sort actions by cycle
        sorted_actions = sorted(actions, key=lambda a: a.cycle)
        
        simulation_results = []
        current_time = 0
        active_processes = {}  # pid -> (resource, end_time)
        
        for action in sorted_actions:
            # Advance time to action cycle
            current_time = max(current_time, action.cycle)
            
            # Check for completed processes
            completed = []
            for pid, (res_name, end_time) in active_processes.items():
                if end_time <= current_time:
                    resource = resource_map[res_name]
                    next_process = resource.release(pid)
                    completed.append(pid)
                    
                    # Grant access to next waiting process
                    if next_process:
                        simulation_results.append((
                            next_process,
                            "GRANTED",
                            current_time,
                            current_time + 1,
                            ActionState.ACCESSED
                        ))
                        active_processes[next_process] = (res_name, current_time + 1)
            
            for pid in completed:
                del active_processes[pid]
            
            resource = resource_map.get(action.resource)
            if not resource:
                continue
            
            # Try to acquire resource
            if resource.acquire(action.pid):
                # Resource acquired successfully
                action.state = ActionState.ACCESSED
                simulation_results.append((
                    action.pid,
                    action.action_type.value,
                    current_time,
                    current_time + 1,
                    ActionState.ACCESSED
                ))
                active_processes[action.pid] = (action.resource, current_time + 1)
            else:
                # Resource not available, process waits
                action.state = ActionState.WAITING
                simulation_results.append((
                    action.pid,
                    action.action_type.value,
                    current_time,
                    current_time + 1,
                    ActionState.WAITING
                ))
        
        return simulation_results

