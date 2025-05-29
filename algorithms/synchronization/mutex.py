from typing import List, Dict, Tuple
from models.process import Process
from models.resource import Resource
from models.action import Action, ActionState

class Mutex:
    @staticmethod
    def simulate(processes: List[Process], resources: List[Resource], 
                actions: List[Action]) -> List[Tuple[str, str, int, int, ActionState]]:
        if not actions:
            return []
        
        resource_map = {r.name: r for r in resources}
        
        sorted_actions = sorted(actions, key=lambda a: a.cycle)
        
        simulation_results = []
        current_time = 0
        
        for action in sorted_actions:
            current_time = max(current_time, action.cycle)
            
            resource = resource_map.get(action.resource)
            if not resource:
                continue
            
            if resource.acquire(action.pid):
                action.state = ActionState.ACCESSED
                simulation_results.append((
                    action.pid, 
                    action.action_type.value, 
                    current_time, 
                    current_time + 1, 
                    ActionState.ACCESSED
                ))
                
                next_process = resource.release(action.pid)
                current_time += 1
                
                if next_process:
                    simulation_results.append((
                        next_process,
                        "GRANTED",
                        current_time,
                        current_time + 1,
                        ActionState.ACCESSED
                    ))
                    current_time += 1
            else:
                action.state = ActionState.WAITING
                simulation_results.append((
                    action.pid,
                    action.action_type.value,
                    current_time,
                    current_time + 1,
                    ActionState.WAITING
                ))
        
        return simulation_results

