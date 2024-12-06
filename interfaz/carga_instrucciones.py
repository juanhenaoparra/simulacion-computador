import tkinter as tk
from compilador.compilador import Compilador
from cpu.control_unit.control_unit import ControlUnit, ControlUnitMode
from cpu.memory.memory import Memory, MemoryType
from cpu.memory.register import Register
from cpu.models.events import EventBus,ResourceChange, ResourceType
from cpu.models.directions import number_to_binary

class TextStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer")
        self.root.geometry("800x500")  # Tamaño de la ventana
        self.root.configure(bg="#2C2C34")  # Fondo general oscuro

        # Crear secciones principales
        left_frame = tk.Frame(self.root, bg="#141414")  # Fondo gris oscuro
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        left_frame.grid_columnconfigure(0, weight=1)  
        left_frame.grid_columnconfigure(1, weight=1) 
        left_frame.grid_rowconfigure(1, weight=1)     # Fila ALU
        left_frame.grid_rowconfigure(5, weight=1)     # Fila Registros
        

        right_frame = tk.Frame(self.root, bg="#1C3A40")  # Fondo azul oscuro
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Sección izquierda (ALU, registros, CU, etc.)
        operando_a = tk.Label(left_frame, text="A: None", fg="#C8C8C8", bg="#2C2C34")
        operando_a.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        operando_b = tk.Label(left_frame, text="B: None", fg="#C8C8C8", bg="#2C2C34")
        operando_b.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        # ALU
        alu_label = tk.Label(left_frame, text="ALU", fg="black", bg="#6CCFF6", width=45, height=7)
        alu_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Salida ALU
        salida_alu = tk.Label(left_frame, text="OUT: None", fg="#C8C8C8", bg="#2C2C34")
        salida_alu.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # CU (Unidad de Control)
        cu_label = tk.Label(left_frame, text="CU", fg="black", bg="#32CD32", width=45, height=7)
        cu_label.grid(row=3, column=0, columnspan=2, pady=10)
        #donde se muestra el PC, MAR, MBR, IR
        frame_registros = tk.Frame(left_frame,bg="#141414",width=50, height=7)
        frame_registros.grid(row=4, column=0, columnspan=4, pady=5)
        frame_registros.grid_rowconfigure(1, weight=1)
        frame_registros.grid_rowconfigure(2, weight=1)
        frame_registros.grid_rowconfigure(3, weight=1)
        frame_registros.grid_rowconfigure(4, weight=1)

        # Label para el PC
        self.pc=tk.Label( frame_registros, text="PC: 00", bg="#6CCFF6", fg="black",width=45)
        self.pc.grid(row=1,  column=0, columnspan=2, pady=10)
        EventBus.subscribe(ResourceType.PC, self.set_value)

        # label para el MAR
        self.mar=tk.Label(frame_registros, text="MAR: None", bg="#6CCFF6", fg="black",width=45)
        self.mar.grid(row=2,  column=0, columnspan=2, pady=10)
        EventBus.subscribe(ResourceType.MAR, self.set_value, lambda change: change.event == "set_value")
        
        # Label para el MBR
        self.mbr=tk.Label(frame_registros, text="MBR: None", bg="#6CCFF6", fg="black",width=45)
        self.mbr.grid(row=3,  column=0, columnspan=2, pady=10)
        EventBus.subscribe(ResourceType.MBR, self.set_value, lambda change: change.event == "set_value")
        
        # label para el IR
        self.ir=tk.Label(frame_registros, text="IR: None", bg="#6CCFF6", fg="black",width=45)
        self.ir.grid(row=4,  column=0, columnspan=2, pady=10)
        EventBus.subscribe(ResourceType.IR, self.set_value, lambda change: change.event == "set_value")
        # Registros
        registers_frame = tk.Frame(left_frame, bg="#2C2C34")
        registers_frame.grid(row=5, column=0, columnspan=4, pady=5)

        for i in range(8):  # Registros individuales (R0 a R15)
            tk.Label(registers_frame, text=f"R{i:02}: None", fg="#C8C8C8", bg="#2C2C34", width=40).grid(row=i, column=0, sticky="w", padx=5)
            tk.Label(registers_frame, text=f"R{i+8:02}: None", fg="#C8C8C8", bg="#2C2C34", width=40).grid(row=i, column=1, sticky="w", padx=5)

        # Sección derecha (Memoria de datos y programa)
        # Memoria de datos
        data_memory_frame = tk.Frame(right_frame, bg="#32CD32")
        data_memory_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        tk.Label(data_memory_frame, text="Data Memory", fg="black", bg="#32CD32", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4)
        x=1
        self.data_memory_labels = [] 
        for i in range(10):
            if i%2==0 and i!=0:
                x+=1
            row = x 
            col = i % 2  # Columna 0-3
            label=tk.Label(data_memory_frame, text=f"{i}: None", bg="#C8FFFF", width=20).grid(row=row, column=col, padx=5, pady=5)
            self.data_memory_labels.append(label)

        # Memoria de programa
        program_memory_frame = tk.Frame(right_frame, bg="#32CD32")
        program_memory_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        tk.Label(program_memory_frame, text="Program Memory", fg="black", bg="#32CD32", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4)
        self.program_memory_labels = []  # Lista para almacenar las etiquetas
        for i in range(10):
            if i%2==0 and i!=0:
                x+=1
            row = x 
            col = i % 2  # Columna 0-1
            label=tk.Label(program_memory_frame, text=f"{i:02}", bg="#C8FFFF", width=40)
            label.grid(row=row, column=col, padx=5, pady=5)
            self.program_memory_labels.append(label)
        # Botones inferiores
        button_frame = tk.Frame(self.root, bg="#2C2C34", width=50)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="Guardar Texto", bg="#6CCFF6", fg="black", width=10, command=self.save_text).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Next", bg="#6CCFF6", fg="black", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Load", bg="#6CCFF6", fg="black", width=10).pack(side=tk.LEFT, padx=5)
        # Cuadro de texto
        self.text_box = tk.Text(self.root, width=25, height=20, bg="white", fg="black")  # Cambié height de 50 a 30
        self.text_box.pack(pady=10)


        # Etiqueta para mensajes
        self.message_label = tk.Label(self.root, text="", fg="green", bg="#2C2C34")
        self.message_label.pack(pady=5)

        # Almacén de texto
        self.text_storage = []

    def save_text(self):
        """
        Obtiene el texto del cuadro de texto, lo procesa con la clase Compilador
        y muestra el resultado en la consola.
        """
        # Obtener el texto ingresado y separarlo en líneas
        raw_text = self.text_box.get("1.0", tk.END).strip()
        if not raw_text:
            self.message_label.config(text="El cuadro de texto está vacío.", fg="red")
            return

        self.text_storage = raw_text.splitlines()

        # Crear un objeto de la clase Compilador
        comp = Compilador()

        try:
            # Procesar el texto ingresado para separar instrucciones y operandos
            resultado = comp.separador(self.text_storage)
            if resultado:
                instrucciones_raw, operandos_raw = resultado
                instrucciones_procesadas = []
                operandos = ""
                operandos = ""
                for i in range(0, len(instrucciones_raw)):
                    instruccion = comp.tipoinstruccion(instrucciones_raw[i])
                    operandos = comp.convertir_comaflotante(operandos_raw[i])
                    instrucciones_procesadas.append(instruccion + operandos[0] + operandos[1])
                    self.funcion(instrucciones_procesadas)
                # Mostrar resultados en la consola
                self.message_label.config(
                    text="Texto procesado correctamente.", fg="green"
                )
            else:
                self.message_label.config(
                    text="Error al procesar el texto. Verifica la entrada.", fg="red"
                )
        except Exception as e:
            print(f"Error: {e}")
            self.message_label.config(text=f"Error al procesar: {e}", fg="red")

        try:
            mp = Memory(MemoryType.PROGRAM)
            for i in range(0, len(instrucciones_procesadas)):
                mp.write(number_to_binary(i, 28), instrucciones_procesadas[i])
                
            control_unit = ControlUnit()
            EventBus.set_debug(True)
            control_unit.run(mode=ControlUnitMode.RUN, delay=1)
        except Exception as e:
            print(f"Error al inicializar CPU: {e}")
            self.message_label.config(text=f"Error al inicializar CPU: {e}", fg="red")
    def set_value(self, change: ResourceChange):
        """
        Establece el valor en el label correspondiente según el tipo de recurso.
        """
        if F"{change.resource_type}" == "ResourceType.PC":
            value = change.metadata.get("position")
        else:
            value = change.metadata.get("value")

        # Programar actualización usando after
        self.root.after(0, self._update_label, change.resource_type, value)

    def _update_label(self, resource_type, value):
        """
        Actualiza directamente el texto del label según el tipo de recurso.
        """
        if F"{resource_type}" == "ResourceType.PC":
            self.pc.config(text=f"PC: {value}")
        elif F"{resource_type}" == "ResourceType.MAR":
            self.mar.config(text=f"MAR: {value}")
        elif F"{resource_type}" == "ResourceType.MBR":
            self.mbr.config(text=f"MBR: {value}")
        elif F"{resource_type}" == "ResourceType.IR":
            self.ir.config(text=f"IR: {value}")

    def funcion(self, instruccion):
        """
        Actualiza las instrucciones en la memoria de programa.
        """
        self.root.after(0, self._update_label_memory, instruccion)

    def _update_label_memory(self, memory):
        """
        Actualiza todos los labels de memoria de programa en batch usando after.
        """
        for i in range(len(self.program_memory_labels)):
            value = memory[i] if i < len(memory) else "None"
            # Programar actualizaciones de cada label
            self.root.after(0, self.program_memory_labels[i].config, {"text": f"{i:02}: {value}"})

                    
        
