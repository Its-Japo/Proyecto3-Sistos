import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

class GanttChart:
    def __init__(self, parent):
        self.parent = parent
        self.colors = {}
        self.setup_ui()
    
    def setup_ui(self):
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.main_frame, bg='white', height=200)
        
        h_scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, 
                                   command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, 
                                   command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, 
                             yscrollcommand=v_scrollbar.set)
        
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.time_label = ttk.Label(self.main_frame, text="Ciclo: 0", 
                                   font=('Arial', 12, 'bold'))
        self.time_label.pack(side=tk.TOP, pady=5)
    
    def get_color(self, process_id: str) -> str:
        base_colors = {
            'P1': '#FF6B6B', 'P2': '#4ECDC4', 'P3': '#45B7D1', 
            'P4': '#96CEB4', 'P5': '#FFEAA7', 'P6': '#DDA0DD'
        }
        
        if "_ESPERA" in process_id or "WAITING" in process_id:
            base_pid = process_id.split('_')[0]
            return '#808080'  
        elif "_EXITO" in process_id or "ACCESSED" in process_id:
            base_pid = process_id.split('_')[0]
            return base_colors.get(base_pid, '#00FF00') 
        else:
            if process_id not in self.colors:
                colors = list(base_colors.values())
                self.colors[process_id] = colors[len(self.colors) % len(colors)]
            return self.colors[process_id]
    
    def clear(self):
        self.canvas.delete("all")
        self.colors.clear()
        self.time_label.config(text="Ciclo: 0")
    
    def draw_schedule(self, schedule: List[Tuple], current_time: int = None):
        self.canvas.delete("all")
        
        if not schedule:
            return
        
        block_height = 40
        block_spacing = 5
        time_scale = 30
        start_x = 50
        start_y = 50
        
        self.canvas.create_text(start_x, 20, text="🟢 Acceso Exitoso", 
                               font=('Arial', 10), anchor='w', fill='green')
        self.canvas.create_text(start_x + 150, 20, text="🔴 En Espera", 
                               font=('Arial', 10), anchor='w', fill='red')
        
        max_time = max(end for _, _, end in schedule) if schedule else 10
        
        for i in range(max_time + 1):
            x = start_x + i * time_scale
            self.canvas.create_line(x, start_y - 10, x, start_y + 200, 
                                   fill='lightgray', dash=(2, 2))
            self.canvas.create_text(x, start_y - 15, text=str(i), 
                                   font=('Arial', 8))
        
        y_positions = {}
        current_y = start_y
        
        for process_id, start_time, end_time in schedule:
            base_pid = process_id.split('_')[0] 
            
            if base_pid not in y_positions:
                y_positions[base_pid] = current_y
                current_y += block_height + block_spacing
            
            y = y_positions[base_pid]
            x1 = start_x + start_time * time_scale
            x2 = start_x + end_time * time_scale
            
            color = self.get_color(process_id)
            
            if "WAITING" in process_id or "_ESPERA" in process_id:
                self.canvas.create_rectangle(x1, y, x2, y + block_height, 
                                           fill=color, outline='red', width=2,
                                           stipple='gray50')
                text_color = 'white'
                status_text = "WAIT"
            else:
                self.canvas.create_rectangle(x1, y, x2, y + block_height, 
                                           fill=color, outline='green', width=2)
                text_color = 'black'
                status_text = "OK"
            
            self.canvas.create_text((x1 + x2) / 2, y + block_height / 2 - 5, 
                                   text=base_pid, font=('Arial', 9, 'bold'),
                                   fill=text_color)
            self.canvas.create_text((x1 + x2) / 2, y + block_height / 2 + 5, 
                                   text=status_text, font=('Arial', 8),
                                   fill=text_color)
        
        # Etiquetas de procesos
        for process_id, y in y_positions.items():
            self.canvas.create_text(25, y + block_height / 2, text=process_id, 
                                   font=('Arial', 10, 'bold'))
        
        # Línea de tiempo actual
        if current_time is not None:
            x = start_x + current_time * time_scale
            self.canvas.create_line(x, start_y - 20, x, current_y, 
                                   fill='red', width=3)
            self.time_label.config(text=f"Ciclo: {current_time}")
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def animate_schedule(self, schedule: List[Tuple], delay: int = 1000):
        if not schedule:
            return
        
        self.clear()
        max_time = max(end for _, _, end in schedule)
        
        def update_animation(current_time):
            visible_schedule = []
            for process_id, start_time, end_time in schedule:
                if start_time < current_time:
                    visible_end = min(end_time, current_time)
                    visible_schedule.append((process_id, start_time, visible_end))
            
            self.draw_schedule(visible_schedule, current_time)
            
            if current_time <= max_time:
                self.parent.after(delay, lambda: update_animation(current_time + 1))
        
        update_animation(0)

