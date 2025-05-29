import tkinter as tk
from tkinter import ttk, messagebox
import sys
import traceback
from gui.scheduling_tab import SchedulingTab
from gui.synchronization_tab import SynchronizationTab

class MainWindow:
    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.title("Simulador de Sistemas Operativos")
            self.root.geometry("1200x800")
            self.root.minsize(1000, 600)
            
            self.root.report_callback_exception = self.handle_exception
            
            style = ttk.Style()
            style.theme_use('clam')
            
            self.setup_ui()
            
        except Exception as e:
            self.show_critical_error("Error al inicializar la aplicación", e)
            sys.exit(1)
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.exit(1)
        
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        messagebox.showerror(
            "Error Inesperado",
            f"Ocurrió un error inesperado:\n\n{exc_value}\n\n"
            f"Por favor verifique su entrada e intente nuevamente.\n"
            f"Si el problema persiste, contacte soporte técnico."
        )
        
        print(f"Excepción no manejada: {error_msg}", file=sys.stderr)
    
    def show_critical_error(self, message, exception):
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error Crítico", f"{message}\n\nError: {str(exception)}")
            root.destroy()
        except:
            print(f"Error Crítico: {message} - {str(exception)}", file=sys.stderr)
    
    def setup_ui(self):
        try:
            title_frame = ttk.Frame(self.root)
            title_frame.pack(fill=tk.X, padx=10, pady=10)
            
            title_label = ttk.Label(title_frame, 
                                   text="Simulador de Sistemas Operativos", 
                                   font=('Arial', 16, 'bold'))
            title_label.pack()
            
            subtitle_label = ttk.Label(title_frame, 
                                      text="Calendarización de Procesos y Mecanismos de Sincronización", 
                                      font=('Arial', 10))
            subtitle_label.pack()
            
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            try:
                scheduling_frame = ttk.Frame(self.notebook)
                self.notebook.add(scheduling_frame, text="Calendarización de Procesos")
                self.scheduling_tab = SchedulingTab(scheduling_frame)
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear pestaña de calendarización: {str(e)}")
            
            try:
                synchronization_frame = ttk.Frame(self.notebook)
                self.notebook.add(synchronization_frame, text="Sincronización")
                self.synchronization_tab = SynchronizationTab(synchronization_frame)
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear pestaña de sincronización: {str(e)}")
            
            self.status_bar = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN)
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
            
        except Exception as e:
            self.show_critical_error("Error al configurar la interfaz de usuario", e)
            raise
    
    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Aplicación terminada por el usuario")
        except Exception as e:
            self.show_critical_error("Error de ejecución de la aplicación", e)

