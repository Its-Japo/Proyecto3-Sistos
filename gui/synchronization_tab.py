import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List

from algorithms.synchronization.mutex import Mutex
from algorithms.synchronization.semaphore import Semaphore
from models.process import Process
from models.resource import Resource
from models.action import Action, ActionState
from utils.file_loader import FileLoader, FileValidationError
from gui.gantt_chart import GanttChart

class SynchronizationTab:
    def __init__(self, parent):
        self.parent = parent
        self.processes: List[Process] = []
        self.resources: List[Resource] = []
        self.actions: List[Action] = []
        self.current_simulation = []
        self.animation_running = False
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        control_frame = ttk.LabelFrame(main_frame, text="Panel de Control", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        file_frame = ttk.Frame(control_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        process_file_frame = ttk.Frame(file_frame)
        process_file_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(process_file_frame, text="Procesos:").pack(side=tk.LEFT, anchor=tk.W)
        self.process_file_var = tk.StringVar()
        ttk.Entry(process_file_frame, textvariable=self.process_file_var, width=40).pack(
            side=tk.LEFT, padx=(5, 5))
        ttk.Button(process_file_frame, text="Examinar", 
                  command=lambda: self.browse_file(self.process_file_var)).pack(side=tk.LEFT)
        
        resource_file_frame = ttk.Frame(file_frame)
        resource_file_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(resource_file_frame, text="Recursos:").pack(side=tk.LEFT, anchor=tk.W)
        self.resource_file_var = tk.StringVar()
        ttk.Entry(resource_file_frame, textvariable=self.resource_file_var, width=40).pack(
            side=tk.LEFT, padx=(5, 5))
        ttk.Button(resource_file_frame, text="Examinar", 
                  command=lambda: self.browse_file(self.resource_file_var)).pack(side=tk.LEFT)
        
        action_file_frame = ttk.Frame(file_frame)
        action_file_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(action_file_frame, text="Acciones:").pack(side=tk.LEFT, anchor=tk.W)
        self.action_file_var = tk.StringVar()
        ttk.Entry(action_file_frame, textvariable=self.action_file_var, width=40).pack(
            side=tk.LEFT, padx=(5, 5))
        ttk.Button(action_file_frame, text="Examinar", 
                  command=lambda: self.browse_file(self.action_file_var)).pack(side=tk.LEFT)
        
        ttk.Button(file_frame, text="Cargar Todos los Archivos", 
                  command=self.load_all_files).pack(pady=(5, 0))
        
        sync_frame = ttk.Frame(control_frame)
        sync_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(sync_frame, text="Mecanismo de Sincronización:").pack(side=tk.LEFT)
        self.sync_mechanism_var = tk.StringVar(value="Mutex")
        sync_combo = ttk.Combobox(sync_frame, textvariable=self.sync_mechanism_var,
                                 values=["Mutex", "Semáforo"], state="readonly", width=15)
        sync_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Simular", 
                  command=self.simulate).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Animar", 
                  command=self.animate_simulation).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Detener", 
                  command=self.stop_animation).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Limpiar", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=(0, 5))
        
        info_container = ttk.Frame(main_frame)
        info_container.pack(fill=tk.X, pady=(0, 10))
        
        process_info_frame = ttk.LabelFrame(info_container, text="Procesos", padding=5)
        process_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        process_columns = ("PID", "Tiempo Ráfaga", "Tiempo Llegada", "Prioridad")
        self.process_tree = ttk.Treeview(process_info_frame, columns=process_columns, 
                                        show="headings", height=4)
        
        for col in process_columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=80, anchor=tk.CENTER)
        
        self.process_tree.pack(fill=tk.BOTH, expand=True)
        
        resource_info_frame = ttk.LabelFrame(info_container, text="Recursos", padding=5)
        resource_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        resource_columns = ("Nombre", "Cantidad", "Disponible")
        self.resource_tree = ttk.Treeview(resource_info_frame, columns=resource_columns, 
                                         show="headings", height=4)
        
        for col in resource_columns:
            self.resource_tree.heading(col, text=col)
            self.resource_tree.column(col, width=80, anchor=tk.CENTER)
        
        self.resource_tree.pack(fill=tk.BOTH, expand=True)
        
        action_info_frame = ttk.LabelFrame(info_container, text="Acciones", padding=5)
        action_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        action_columns = ("PID", "Acción", "Recurso", "Ciclo")
        self.action_tree = ttk.Treeview(action_info_frame, columns=action_columns, 
                                       show="headings", height=4)
        
        for col in action_columns:
            self.action_tree.heading(col, text=col)
            self.action_tree.column(col, width=80, anchor=tk.CENTER)
        
        self.action_tree.pack(fill=tk.BOTH, expand=True)
        
        results_frame = ttk.LabelFrame(main_frame, text="Resultados de Simulación", padding=10)
        results_frame.pack(fill=tk.X, pady=(0, 10))
        
        result_columns = ("PID", "Acción", "Tiempo Inicio", "Tiempo Fin", "Estado")
        self.result_tree = ttk.Treeview(results_frame, columns=result_columns, 
                                       show="headings", height=6)
        
        for col in result_columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=100, anchor=tk.CENTER)
        
        result_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, 
                                        command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=result_scrollbar.set)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        timeline_frame = ttk.LabelFrame(main_frame, text="Línea de Tiempo", padding=10)
        timeline_frame.pack(fill=tk.BOTH, expand=True)
        
        self.timeline_chart = GanttChart(timeline_frame)
    
    def browse_file(self, var):
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            var.set(file_path)
    
    def load_all_files(self):
        try:
            if self.process_file_var.get():
                self.processes = FileLoader.load_processes(self.process_file_var.get())
                self.update_process_table()
            
            if self.resource_file_var.get():
                self.resources = FileLoader.load_resources(self.resource_file_var.get())
                self.update_resource_table()
            
            if self.action_file_var.get():
                self.actions = FileLoader.load_actions(self.action_file_var.get())
                self.update_action_table()
            
            messagebox.showinfo("Éxito", 
                              f"Se cargaron {len(self.processes)} procesos, "
                              f"{len(self.resources)} recursos, "
                              f"{len(self.actions)} acciones")
        
        except FileValidationError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivos: {str(e)}")
    
    def update_process_table(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        for process in self.processes:
            values = (process.pid, process.burst_time, process.arrival_time, process.priority)
            self.process_tree.insert("", tk.END, values=values)
    
    def update_resource_table(self):
        for item in self.resource_tree.get_children():
            self.resource_tree.delete(item)
        
        for resource in self.resources:
            values = (resource.name, resource.count, resource.available)
            self.resource_tree.insert("", tk.END, values=values)
    
    def update_action_table(self):
        for item in self.action_tree.get_children():
            self.action_tree.delete(item)
        
        for action in self.actions:
            values = (action.pid, action.action_type.value, action.resource, action.cycle)
            self.action_tree.insert("", tk.END, values=values)
    
    def update_result_table(self):
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        for result in self.current_simulation:
            pid, action, start_time, end_time, state = result
            values = (pid, action, start_time, end_time, state.value)
            self.result_tree.insert("", tk.END, values=values)
    
    def simulate(self):
        if not self.processes or not self.resources or not self.actions:
            messagebox.showerror("Error", "Por favor cargue todos los archivos primero")
            return
        
        mechanism = self.sync_mechanism_var.get()
        
        try:
            for resource in self.resources:
                resource.available = resource.count
                resource.waiting_processes.clear()
            
            if mechanism == "Mutex":
                self.current_simulation = Mutex.simulate(
                    self.processes.copy(), self.resources.copy(), self.actions.copy())
            else:
                self.current_simulation = Semaphore.simulate(
                    self.processes.copy(), self.resources.copy(), self.actions.copy())
            
            self.update_result_table()
            
            timeline_data = []
            for pid, action, start_time, end_time, state in self.current_simulation:
                timeline_data.append((f"{pid}_{action}", start_time, end_time))
            
            self.timeline_chart.draw_schedule(timeline_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al simular: {str(e)}")
    
    def animate_simulation(self):
        if not self.current_simulation:
            messagebox.showerror("Error", "Por favor ejecute la simulación primero")
            return
        
        self.animation_running = True
        
        timeline_data = []
        for pid, action, start_time, end_time, state in self.current_simulation:
            color_suffix = "_EXITO" if state == ActionState.ACCESSED else "_ESPERA"
            timeline_data.append((f"{pid}_{action}{color_suffix}", start_time, end_time))
        
        self.timeline_chart.animate_schedule(timeline_data, delay=1000)
    
    def stop_animation(self):
        self.animation_running = False
    
    def clear_all(self):
        self.processes.clear()
        self.resources.clear()
        self.actions.clear()
        self.current_simulation.clear()
        self.animation_running = False
        
        self.update_process_table()
        self.update_resource_table()
        self.update_action_table()
        self.update_result_table()
        self.timeline_chart.clear()

