from typing import List
from models.process import Process
from models.resource import Resource
from models.action import Action, ActionType
import os
import re

class FileValidationError(Exception):
    pass

class FileLoader:
    @staticmethod
    def validate_file_exists(file_path: str) -> None:
        if not file_path:
            raise FileValidationError("La ruta del archivo está vacía")
        
        if not os.path.exists(file_path):
            raise FileValidationError(f"El archivo no existe: {file_path}")
        
        if not os.path.isfile(file_path):
            raise FileValidationError(f"La ruta no es un archivo: {file_path}")
        
        if not os.access(file_path, os.R_OK):
            raise FileValidationError(f"El archivo no se puede leer: {file_path}")
    
    @staticmethod
    def validate_process_line(line: str, line_number: int) -> List[str]:
        if not line.strip():
            raise FileValidationError(f"Línea {line_number}: Línea vacía")
        
        parts = [part.strip() for part in line.split(',')]
        
        if len(parts) < 4:
            raise FileValidationError(
                f"Línea {line_number}: Se esperan 4 campos (PID, BT, AT, Prioridad), se encontraron {len(parts)}"
            )
        
        pid = parts[0]
        if not pid:
            raise FileValidationError(f"Línea {line_number}: El PID no puede estar vacío")
        
        if not re.match(r'^[A-Za-z0-9_-]+$', pid):
            raise FileValidationError(
                f"Línea {line_number}: El PID '{pid}' contiene caracteres inválidos"
            )
        
        try:
            burst_time = int(parts[1])
            if burst_time <= 0:
                raise FileValidationError(
                    f"Línea {line_number}: El tiempo de ráfaga debe ser positivo, se obtuvo {burst_time}"
                )
        except ValueError:
            raise FileValidationError(
                f"Línea {line_number}: El tiempo de ráfaga debe ser un entero, se obtuvo '{parts[1]}'"
            )
        
        try:
            arrival_time = int(parts[2])
            if arrival_time < 0:
                raise FileValidationError(
                    f"Línea {line_number}: El tiempo de llegada no puede ser negativo, se obtuvo {arrival_time}"
                )
        except ValueError:
            raise FileValidationError(
                f"Línea {line_number}: El tiempo de llegada debe ser un entero, se obtuvo '{parts[2]}'"
            )
        
        try:
            priority = int(parts[3])
            if priority < 0:
                raise FileValidationError(
                    f"Línea {line_number}: La prioridad no puede ser negativa, se obtuvo {priority}"
                )
        except ValueError:
            raise FileValidationError(
                f"Línea {line_number}: La prioridad debe ser un entero, se obtuvo '{parts[3]}'"
            )
        
        return parts
    
    @staticmethod
    def load_processes(file_path: str) -> List[Process]:
        try:
            FileLoader.validate_file_exists(file_path)
            
            processes = []
            seen_pids = set()
            line_number = 0
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line_number += 1
                    line = line.strip()
                    
                    if not line or line.startswith('#'):
                        continue
                    
                    try:
                        parts = FileLoader.validate_process_line(line, line_number)
                        
                        pid = parts[0]
                        burst_time = int(parts[1])
                        arrival_time = int(parts[2])
                        priority = int(parts[3])
                        
                        if pid in seen_pids:
                            raise FileValidationError(
                                f"Línea {line_number}: PID duplicado '{pid}'"
                            )
                        seen_pids.add(pid)
                        
                        processes.append(Process(pid, burst_time, arrival_time, priority))
                        
                    except FileValidationError:
                        raise
                    except Exception as e:
                        raise FileValidationError(
                            f"Línea {line_number}: Error inesperado - {str(e)}"
                        )
            
            if not processes:
                raise FileValidationError("No se encontraron procesos válidos en el archivo")
            
            return processes
            
        except FileValidationError:
            raise
        except UnicodeDecodeError:
            raise FileValidationError(f"Error de codificación del archivo: {file_path}")
        except PermissionError:
            raise FileValidationError(f"Permiso denegado: {file_path}")
        except Exception as e:
            raise FileValidationError(f"Error inesperado cargando procesos: {str(e)}")
    
    @staticmethod
    def load_resources(file_path: str) -> List[Resource]:
        try:
            FileLoader.validate_file_exists(file_path)
            
            resources = []
            seen_names = set()
            line_number = 0
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line_number += 1
                    line = line.strip()
                    
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = [part.strip() for part in line.split(',')]
                    
                    if len(parts) < 2:
                        raise FileValidationError(
                            f"Línea {line_number}: Se esperan 2 campos (Nombre, Cantidad), se encontraron {len(parts)}"
                        )
                    
                    name = parts[0]
                    if not name:
                        raise FileValidationError(f"Línea {line_number}: El nombre del recurso no puede estar vacío")
                    
                    if not re.match(r'^[A-Za-z0-9_-]+$', name):
                        raise FileValidationError(
                            f"Línea {line_number}: El nombre del recurso '{name}' contiene caracteres inválidos"
                        )
                    
                    if name in seen_names:
                        raise FileValidationError(
                            f"Línea {line_number}: Nombre de recurso duplicado '{name}'"
                        )
                    seen_names.add(name)
                    
                    try:
                        count = int(parts[1])
                        if count <= 0:
                            raise FileValidationError(
                                f"Línea {line_number}: La cantidad del recurso debe ser positiva, se obtuvo {count}"
                            )
                    except ValueError:
                        raise FileValidationError(
                            f"Línea {line_number}: La cantidad del recurso debe ser un entero, se obtuvo '{parts[1]}'"
                        )
                    
                    resources.append(Resource(name, count))
            
            if not resources:
                raise FileValidationError("No se encontraron recursos válidos en el archivo")
            
            return resources
            
        except FileValidationError:
            raise
        except Exception as e:
            raise FileValidationError(f"Error inesperado cargando recursos: {str(e)}")
    
    @staticmethod
    def load_actions(file_path: str) -> List[Action]:
        try:
            FileLoader.validate_file_exists(file_path)
            
            actions = []
            line_number = 0
            
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line_number += 1
                    line = line.strip()
                    
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = [part.strip() for part in line.split(',')]
                    
                    if len(parts) < 4:
                        raise FileValidationError(
                            f"Línea {line_number}: Se esperan 4 campos (PID, Acción, Recurso, Ciclo), se encontraron {len(parts)}"
                        )
                    
                    pid = parts[0]
                    if not pid:
                        raise FileValidationError(f"Línea {line_number}: El PID no puede estar vacío")
                    
                    action_str = parts[1].upper()
                    try:
                        action_type = ActionType(action_str)
                    except ValueError:
                        valid_actions = [action.value for action in ActionType]
                        raise FileValidationError(
                            f"Línea {line_number}: Acción inválida '{parts[1]}'. Acciones válidas: {valid_actions}"
                        )
                    
                    resource = parts[2]
                    if not resource:
                        raise FileValidationError(f"Línea {line_number}: El recurso no puede estar vacío")
                    
                    try:
                        cycle = int(parts[3])
                        if cycle < 0:
                            raise FileValidationError(
                                f"Línea {line_number}: El ciclo no puede ser negativo, se obtuvo {cycle}"
                            )
                    except ValueError:
                        raise FileValidationError(
                            f"Línea {line_number}: El ciclo debe ser un entero, se obtuvo '{parts[3]}'"
                        )
                    
                    actions.append(Action(pid, action_type, resource, cycle))
            
            if not actions:
                raise FileValidationError("No se encontraron acciones válidas en el archivo")
            
            return actions
            
        except FileValidationError:
            raise
        except Exception as e:
            raise FileValidationError(f"Error inesperado cargando acciones: {str(e)}")

