import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List

from algorithms.scheduling.fifo import FIFO
from algorithms.scheduling.sjf import SJF
from algorithms.scheduling.srt import SRT
from algorithms.scheduling.round_robin import RoundRobin
from algorithms.scheduling.priority import Priority
from models.process import Process
from utils.file_loader import FileLoader, FileValidationError
from gui.gantt_chart import GanttChart

class SchedulingTab:
    def __init__(self, parent):
        self.parent = parent
        self.processes: List[Process] = []
        self.current_schedule = []
        self.animation_running = False
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        control_frame = ttk.LabelFrame(main_frame, text="Panel de Control", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        file_frame = ttk.Frame(control_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_frame, text="Archivo de Procesos:").pack(side=tk.LEFT)
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=50).pack(
            side=tk.LEFT, padx=(5, 5))
        ttk.Button(file_frame, text="Examinar", 
                  command=self.browse_file).pack(side=tk.LEFT)
        ttk.Button(file_frame, text="Cargar", 
                  command=self.load_processes).pack(side=tk.LEFT, padx=(5, 0))
        
        algo_frame = ttk.Frame(control_frame)
        algo_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(algo_frame, text="Algoritmo:").pack(side=tk.LEFT)
        self.algorithm_var = tk.StringVar(value="FIFO")
        algo_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var,
                                 values=["FIFO", "SJF", "SRT", "Round Robin", "Prioridad"],
                                 state="readonly", width=15)
        algo_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(algo_frame, text="Quantum:").pack(side=tk.LEFT)
        self.quantum_var = tk.StringVar(value="2")
        quantum_entry = ttk.Entry(algo_frame, textvariable=self.quantum_var, width=5)
        quantum_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Calcular", 
                  command=self.calculate_schedule).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Animar", 
                  command=self.animate_schedule).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Detener", 
                  command=self.stop_animation).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Limpiar", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=(0, 5))
        
        info_frame = ttk.LabelFrame(main_frame, text="Información de Procesos", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        columns = ("PID", "Tiempo Ráfaga", "Tiempo Llegada", "Prioridad", 
                  "Tiempo Inicio", "Tiempo Finalización", "Tiempo Espera", "Tiempo Retorno")
        self.process_tree = ttk.Treeview(info_frame, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100, anchor=tk.CENTER)
        
        process_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, 
                                         command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=process_scrollbar.set)
        
        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        process_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        metrics_frame = ttk.LabelFrame(main_frame, text="Métricas", padding=10)
        metrics_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.avg_waiting_label = ttk.Label(metrics_frame, text="Tiempo Promedio de Espera: N/A")
        self.avg_waiting_label.pack(anchor=tk.W)
        
        self.avg_turnaround_label = ttk.Label(metrics_frame, text="Tiempo Promedio de Retorno: N/A")
        self.avg_turnaround_label.pack(anchor=tk.W)
        
        gantt_frame = ttk.LabelFrame(main_frame, text="Diagrama de Gantt", padding=10)
        gantt_frame.pack(fill=tk.BOTH, expand=True)
        
        self.gantt_chart = GanttChart(gantt_frame)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar Archivo de Procesos",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def load_processes(self):
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Error", "Por favor seleccione un archivo primero")
            return
        
        try:
            self.processes = FileLoader.load_processes(file_path)
            self.update_process_table()
            messagebox.showinfo("Éxito", f"Se cargaron {len(self.processes)} procesos")
        except FileValidationError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar procesos: {str(e)}")
    
    def update_process_table(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        for process in self.processes:
            values = (
                process.pid,
                process.burst_time,
                process.arrival_time,
                process.priority,
                process.start_time if process.start_time is not None else "N/A",
                process.completion_time if process.completion_time is not None else "N/A",
                process.waiting_time if process.waiting_time is not None else "N/A",
                process.turnaround_time if process.turnaround_time is not None else "N/A"
            )
            self.process_tree.insert("", tk.END, values=values)
    
    def validate_quantum(self):
        try:
            quantum = int(self.quantum_var.get())
            if quantum <= 0:
                raise ValueError("El quantum debe ser positivo")
            if quantum > 100:
                raise ValueError("El quantum es demasiado grande (máximo 100)")
            return quantum
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("El quantum debe ser un entero válido")
            raise
    
    def calculate_schedule(self):
        if not self.processes:
            messagebox.showerror("Error", "Por favor cargue procesos primero")
            return
        
        algorithm = self.algorithm_var.get()
        
        try:
            if algorithm not in ["FIFO", "SJF", "SRT", "Round Robin", "Prioridad"]:
                raise ValueError(f"Algoritmo inválido seleccionado: {algorithm}")
            
            if algorithm == "Round Robin":
                quantum = self.validate_quantum()
                if len(self.processes) == 0:
                    raise ValueError("No hay procesos para calendarizar")
                
                if all(p.burst_time == 0 for p in self.processes):
                    raise ValueError("Todos los procesos tienen tiempo de ráfaga cero")
                
                self.current_schedule = RoundRobin.schedule(self.processes.copy(), quantum)
            else:
                if algorithm == "FIFO":
                    self.current_schedule = FIFO.schedule(self.processes.copy())
                elif algorithm == "SJF":
                    self.current_schedule = SJF.schedule(self.processes.copy())
                elif algorithm == "SRT":
                    self.current_schedule = SRT.schedule(self.processes.copy())
                elif algorithm == "Prioridad":
                    self.current_schedule = Priority.schedule(self.processes.copy())
            
            if not self.current_schedule:
                raise ValueError("El algoritmo produjo una calendarización vacía")
            
            self.update_process_table()
            self.update_metrics()
            self.gantt_chart.draw_schedule(self.current_schedule)
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular calendarización: {str(e)}")
    
    def update_metrics(self):
        if not self.processes:
            return
        
        waiting_times = [p.waiting_time for p in self.processes if p.waiting_time is not None]
        turnaround_times = [p.turnaround_time for p in self.processes if p.turnaround_time is not None]
        
        if waiting_times:
            avg_waiting = sum(waiting_times) / len(waiting_times)
            self.avg_waiting_label.config(text=f"Tiempo Promedio de Espera: {avg_waiting:.2f}")
        
        if turnaround_times:
            avg_turnaround = sum(turnaround_times) / len(turnaround_times)
            self.avg_turnaround_label.config(text=f"Tiempo Promedio de Retorno: {avg_turnaround:.2f}")
    
    def animate_schedule(self):
        if not self.current_schedule:
            messagebox.showerror("Error", "Por favor calcule la calendarización primero")
            return
        
        self.animation_running = True
        self.gantt_chart.animate_schedule(self.current_schedule, delay=1000)
    
    def stop_animation(self):
        self.animation_running = False
    
    def clear_all(self):
        self.processes.clear()
        self.current_schedule.clear()
        self.animation_running = False
        self.update_process_table()
        self.gantt_chart.clear()
        self.avg_waiting_label.config(text="Tiempo Promedio de Espera: N/A")
        self.avg_turnaround_label.config(text="Tiempo Promedio de Retorno: N/A")

