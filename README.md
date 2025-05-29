# Simulador de Sistemas Operativos

Un simulador visual para algoritmos de calendarización de procesos y mecanismos de sincronización desarrollado en Python con Tkinter.

## Características

### Simulador de Calendarización
- **Algoritmos soportados:**
  - First In First Out (FIFO)
  - Shortest Job First (SJF)
  - Shortest Remaining Time (SRT)
  - Round Robin (con quantum configurable)
  - Priority Scheduling

- **Funcionalidades:**
  - Carga dinámica de procesos desde archivos .txt
  - Visualización en tiempo real con Diagrama de Gantt
  - Cálculo de métricas (tiempo promedio de espera y retorno)
  - Animación paso a paso de la ejecución

### Simulador de Sincronización
- **Mecanismos soportados:**
  - Mutex Locks
  - Semáforos

- **Funcionalidades:**
  - Carga de procesos, recursos y acciones desde archivos
  - Visualización de estados ACCESSED y WAITING
  - Simulación de acceso concurrente a recursos
  - Diferenciación visual entre accesos exitosos y esperas

## Requisitos del Sistema

- Python 3.7 o superior
- Tkinter (incluido con Python)
- Módulos estándar: `os`, `re`, `typing`, `dataclasses`, `enum`

## Instalación

1. Clona o descarga el proyecto
2. Asegúrate de tener Python 3.7+ instalado
3. No se requieren dependencias adicionales

## Estructura del Proyecto

```
simulador/
├── main.py                     # Punto de entrada de la aplicación
├── gui/
│   ├── main_window.py         # Ventana principal
│   ├── scheduling_tab.py      # Pestaña de calendarización
│   ├── synchronization_tab.py # Pestaña de sincronización
│   └── gantt_chart.py         # Componente del diagrama de Gantt
├── models/
│   ├── process.py             # Modelo de proceso
│   ├── resource.py            # Modelo de recurso
│   └── action.py              # Modelo de acción
├── algorithms/
│   ├── scheduling/            # Algoritmos de calendarización
│   │   ├── fifo.py
│   │   ├── sjf.py
│   │   ├── srt.py
│   │   ├── round_robin.py
│   │   └── priority.py
│   └── synchronization/       # Mecanismos de sincronización
│       ├── mutex.py
│       └── semaphore.py
├── utils/
│   └── file_loader.py         # Cargador y validador de archivos
└── examples/                  # Archivos de ejemplo
    ├── procesos.txt
    ├── procesos_sync.txt
    ├── recursos_sync.txt
    └── acciones_sync.txt
```

## Uso

### Ejecución
```bash
python main.py
```

### Formatos de Archivo

#### 1. Procesos (para calendarización)
**Formato:** `<PID>, <BT>, <AT>, <Priority>`
- PID: Identificador del proceso
- BT: Tiempo de ráfaga (Burst Time)
- AT: Tiempo de llegada (Arrival Time)
- Priority: Prioridad del proceso

**Ejemplo (procesos.txt):**
```
P1, 8, 0, 1
P2, 4, 1, 2
P3, 9, 2, 3
P4, 5, 3, 1
```

#### 2. Procesos (para sincronización)
**Formato:** `<PID>, <BT>, <AT>, <Priority>`

**Ejemplo (procesos_sync.txt):**
```
P1, 3, 0, 1
P2, 2, 1, 2
P3, 4, 2, 1
```

#### 3. Recursos
**Formato:** `<NOMBRE_RECURSO>, <CONTADOR>`
- NOMBRE_RECURSO: Identificador del recurso
- CONTADOR: Cantidad disponible del recurso

**Ejemplo (recursos_sync.txt):**
```
R1, 1
R2, 2
R3, 3
```

#### 4. Acciones
**Formato:** `<PID>, <ACCION>, <RECURSO>, <CICLO>`
- PID: Identificador del proceso
- ACCION: READ o WRITE
- RECURSO: Nombre del recurso a acceder
- CICLO: Momento en que se ejecuta la acción

**Ejemplo (acciones_sync.txt):**
```
P1, READ, R1, 0
P2, WRITE, R1, 1
P3, READ, R1, 2
P1, WRITE, R2, 3
P2, READ, R2, 3
```

## Guía de Uso

### Simulación de Calendarización

1. **Seleccionar la pestaña "Calendarización de Procesos"**
2. **Cargar archivo de procesos:**
   - Hacer clic en "Examinar" junto a "Archivo de Procesos"
   - Seleccionar un archivo .txt con el formato correcto
   - Hacer clic en "Cargar"
3. **Configurar algoritmo:**
   - Seleccionar algoritmo del menú desplegable
   - Para Round Robin, configurar el quantum
4. **Ejecutar simulación:**
   - Hacer clic en "Calcular" para generar el diagrama
   - Hacer clic en "Animar" para ver la ejecución paso a paso
5. **Visualizar resultados:**
   - Ver métricas de eficiencia
   - Observar el diagrama de Gantt
   - Consultar información detallada de procesos

### Simulación de Sincronización

1. **Seleccionar la pestaña "Sincronización"**
2. **Cargar archivos:**
   - Cargar archivo de procesos
   - Cargar archivo de recursos
   - Cargar archivo de acciones
   - Hacer clic en "Cargar Todos los Archivos"
3. **Configurar mecanismo:**
   - Seleccionar "Mutex" o "Semáforo"
4. **Ejecutar simulación:**
   - Hacer clic en "Simular" para generar resultados
   - Hacer clic en "Animar" para visualización dinámica
5. **Interpretar resultados:**
   - 🟢 **Verde/Sólido:** Acceso exitoso al recurso
   - 🔴 **Gris/Rayado:** Proceso en espera (recurso no disponible)

## Ejemplo de Estados WAITING

Para observar estados de espera, usa estos archivos de ejemplo:

**procesos_sync.txt:**
```
P1, 3, 0, 1
P2, 2, 1, 2
P3, 4, 2, 1
```

**recursos_sync.txt:**
```
R1, 1
```

**acciones_sync.txt:**
```
P1, READ, R1, 0
P2, WRITE, R1, 0
P3, READ, R1, 1
```

En este escenario:
- P1 accede exitosamente a R1 en ciclo 0
- P2 intenta acceder a R1 en ciclo 0 pero debe esperar (WAITING)
- P3 intenta acceder a R1 en ciclo 1 pero debe esperar (WAITING)

## Controles de la Interfaz

### Botones Principales
- **Examinar:** Seleccionar archivos de entrada
- **Cargar:** Cargar y validar archivos
- **Calcular/Simular:** Ejecutar algoritmo seleccionado
- **Animar:** Mostrar ejecución paso a paso
- **Detener:** Parar animación en curso
- **Limpiar:** Reiniciar simulación y limpiar datos

### Visualización
- **Scroll horizontal:** Navegar por líneas de tiempo largas
- **Información de procesos:** Tabla con métricas detalladas
- **Diagrama de Gantt:** Representación visual de la ejecución
- **Contador de ciclos:** Tiempo actual de la simulación

## Validaciones y Manejo de Errores

El simulador incluye validaciones exhaustivas:
- Formato correcto de archivos
- Valores numéricos válidos
- PIDs únicos
- Recursos existentes en acciones
- Parámetros de algoritmos válidos

Los errores se muestran en ventanas de diálogo informativas.

## Métricas Calculadas

### Calendarización
- **Tiempo de Espera:** Tiempo que un proceso espera en la cola
- **Tiempo de Retorno:** Tiempo total desde llegada hasta finalización
- **Tiempo Promedio de Espera:** Media de tiempos de espera
- **Tiempo Promedio de Retorno:** Media de tiempos de retorno

### Sincronización
- **Estados de Acceso:** ACCESSED (exitoso) o WAITING (en espera)
- **Utilización de Recursos:** Visualización de uso concurrente
- **Conflictos de Acceso:** Identificación de bloqueos

## Solución de Problemas

### Errores Comunes

1. **"El archivo no existe"**
   - Verificar que la ruta del archivo sea correcta
   - Asegurar que el archivo tenga extensión .txt

2. **"Formato de archivo inválido"**
   - Revisar que cada línea tenga el número correcto de campos
   - Verificar que no haya espacios extra o caracteres especiales

3. **"PID duplicado"**
   - Asegurar que cada proceso tenga un identificador único

4. **"Recurso no encontrado"**
   - Verificar que todos los recursos mencionados en acciones estén definidos

5. **"Quantum inválido"**
   - Para Round Robin, usar valores enteros positivos

### Consejos de Rendimiento
- Para simulaciones largas, usar archivos con menos de 50 procesos
- Quantum recomendado para Round Robin: 1-10 ciclos
- Evitar recursos con contador 0

## Limitaciones

- Máximo recomendado: 50 procesos por simulación
- Quantum máximo: 100 ciclos
- Tiempo máximo de simulación: 1000 ciclos
- Formatos de archivo: solo .txt con codificación UTF-8

## Contribución

Este proyecto fue desarrollado como parte del curso de Sistemas Operativos de la Universidad del Valle de Guatemala.

## Licencia

Proyecto académico - Universidad del Valle de Guatemala 2025
