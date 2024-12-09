from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, # type: ignore
    QTextEdit, QWidget, QGridLayout, QFrame
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from compilador.compilador import Compilador
from cpu.control_unit.control_unit import ControlUnit, ControlUnitMode
from cpu.memory.memory import Memory, MemoryType
from cpu.models.events import EventBus, ResourceChange, ResourceType
from cpu.models.directions import number_to_binary
from cpu.bus.bus import Commands, BusType
import time


class TextStorageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Computer")
        self.setGeometry(100, 100, 800, 500)
        self.init_ui()
        self.text_storage = []
        self.mp = Memory(MemoryType.PROGRAM)
        self.control_unit = ControlUnit()
        self.instrucciones_procesadas = []
        self.comp = Compilador()
        # Suscripción a eventos de registros
        EventBus.subscribe(ResourceType.MAR,self.crear_lista_eventos,lambda change: change.event == "set_value",)
        EventBus.subscribe(ResourceType.MBR, self.crear_lista_eventos)
        EventBus.subscribe(ResourceType.PC, self.crear_lista_eventos)
        EventBus.subscribe(ResourceType.BUS, self.crear_lista_eventos, lambda change: change.event == "send_command")
        EventBus.subscribe(ResourceType.ALU,self.crear_lista_eventos)
    def init_ui(self):
        # Layout principal
        main_layout = QHBoxLayout()

        # Left Frame
        left_frame = QFrame()
        left_frame.setStyleSheet("background-color: #141414;")

        # Layout de cuadrícula para el Left Frame
        left_layout = QGridLayout()
        left_frame.setLayout(left_layout)

        # Operandos
        self.operando_a = QLabel("a: none")
        self.operando_a.setAlignment(Qt.AlignCenter)
        self.operando_a.setStyleSheet("background-color: #C8FFFF; padding: 5px;")
        self.operando_a.setFixedSize(200, 50)  # Ancho: 200px, Alto: 50px
        left_layout.addWidget(self.operando_a, 0, 0)  # Fila 0, Columna 0

        self.operando_b = QLabel("b: none")
        self.operando_b.setAlignment(Qt.AlignCenter)
        self.operando_b.setStyleSheet("background-color: #C8FFFF; padding: 5px;")
        self.operando_b.setFixedSize(200, 50)
        left_layout.addWidget(self.operando_b, 0, 1)  # Fila 0, Columna 1

        # ALU
        self.alu_label = QLabel("ALU")
        self.alu_label.setAlignment(Qt.AlignCenter)
        self.alu_label.setStyleSheet("background-color: #6CCFF6; font-size: 14px;")
        self.alu_label.setFixedHeight(100)  # Alto: 100px
        left_layout.addWidget(self.alu_label, 1, 0, 1, 2)  # Fila 1, Columnas 0-1

        # Output
        self.output = QLabel("output: None")
        self.output.setAlignment(Qt.AlignCenter)
        self.output.setStyleSheet("background-color: #C8FFFF; padding: 5px;")
        self.output.setFixedSize(400, 50)  # Ancho: 400px, Alto: 50px
        left_layout.addWidget(self.output, 2, 0, 1, 2)  # Fila 2, Columnas 0-1

        # CU
        self.cu_label = QLabel("CU")
        self.cu_label.setAlignment(Qt.AlignCenter)
        self.cu_label.setStyleSheet("background-color: #32CD32; font-size: 14px;")
        self.cu_label.setFixedHeight(100)  # Alto: 100px
        left_layout.addWidget(self.cu_label, 1, 2, 1, 2)  # Fila 1, Columnas 2-3

        # PC y MAR
        self.pc = QLabel("PC: 0000000000000000000000000000")
        self.pc.setAlignment(Qt.AlignCenter)
        self.pc.setStyleSheet("background-color: #6CCFF6; padding: 5px;")
        self.pc.setFixedSize(220, 50)  # Ancho: 220px, Alto: 50px
        left_layout.addWidget(self.pc, 3, 2, 1, 2)  # Fila 3, Columnas 2-3

        self.mar = QLabel("MAR: None")
        self.mar.setAlignment(Qt.AlignCenter)
        self.mar.setStyleSheet("background-color: #6CCFF6; padding: 5px;")
        self.mar.setFixedSize(220, 50)
        left_layout.addWidget(self.mar, 4, 2, 1, 2)  # Fila 4, Columnas 2-3

        # MBR e IR
        self.mbr = QLabel("MBR: None")
        self.mbr.setAlignment(Qt.AlignCenter)
        self.mbr.setStyleSheet("background-color: #6CCFF6; padding: 5px;")
        self.mbr.setFixedSize(400, 50)
        left_layout.addWidget(self.mbr, 3, 0, 1, 2)  # Fila 3, Columnas 0-1

        self.ir = QLabel("IR: None")
        self.ir.setAlignment(Qt.AlignCenter)
        self.ir.setStyleSheet("background-color: #6CCFF6; padding: 5px;")
        self.ir.setFixedSize(400, 50)
        left_layout.addWidget(self.ir, 4, 0, 1, 2)  # Fila 4, Columnas 0-1

        # registros Memory
        registros_memory_layout = QGridLayout()
        registros_memory_frame = QFrame()
        registros_memory_frame.setStyleSheet("background-color: #32CD32;")
        registros_memory_frame.setLayout(registros_memory_layout)
        registros_memory_labels = QLabel("registros Memory")
        registros_memory_labels.setStyleSheet("background-color: #32CD32; padding: 5px;")
        registros_memory_layout.addWidget(registros_memory_labels,0,0)
        self.registros_memory_labels = []
        i=1
        y=1
        for i in range(10):
            label = QLabel(f"{i}: None")
            label.setStyleSheet("background-color: #C8FFFF; padding: 5px;")
            label.setFixedSize(200, 50)
            if i%2 == 0:
                y=y+1
            else:
                y    
            registros_memory_layout.addWidget(label, y , i%2 )
            
            self.registros_memory_labels.append(label)
        left_layout.addWidget(registros_memory_frame, 5 , 0, 1, 4)

        # Right Frame
        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: #1C3A40;")
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        # Data Memory
        data_memory_layout = QGridLayout()
        data_memory_frame = QFrame()
        data_memory_frame.setStyleSheet("background-color: #32CD32;")
        data_memory_frame.setLayout(data_memory_layout)
        data_memory_labels = QLabel("Data Memory")
        data_memory_labels.setStyleSheet("background-color: #32CD32; padding: 5px;")
        data_memory_layout.addWidget(data_memory_labels,0,0)
        self.data_memory_labels = []
        for i in range(6):
            label = QLabel(f"{i}: None")
            label.setStyleSheet("background-color: #C8FFFF; padding: 5px;")
            data_memory_layout.addWidget(label, i+1 , 0 )
            self.data_memory_labels.append(label)
        right_layout.addWidget(data_memory_frame)

        # Program Memory
        program_memory_layout = QGridLayout()
        program_memory_frame = QFrame()
        program_memory_frame.setStyleSheet("background-color: #32CD32;")
        program_memory_frame.setLayout(program_memory_layout)
        program_memory_labels = QLabel("Program Memory")
        program_memory_labels.setStyleSheet("background-color: #32CD32; padding: 5px;")
        program_memory_layout.addWidget(program_memory_labels,0,0)
        self.program_memory_labels = []
        for i in range(6):
            label = QLabel(f"{i:02}: None")
            label.setStyleSheet("background-color: #C8FFFF; padding: 5px;")
            program_memory_layout.addWidget(label, i+1, 0)
            self.program_memory_labels.append(label)
        right_layout.addWidget(program_memory_frame)

        # Text and Buttons
        text_frame = QFrame()
        text_frame.setStyleSheet("background-color: #2C2C34;")
        text_layout = QVBoxLayout()
        text_frame.setLayout(text_layout)

        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Enter instructions here...")
        text_layout.addWidget(self.text_box)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar Texto")
        self.save_button.clicked.connect(self.save_text)
        button_layout.addWidget(self.save_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_text)
        button_layout.addWidget(self.next_button)

        self.load_button = QPushButton("Load")
        button_layout.addWidget(self.load_button)

        text_layout.addLayout(button_layout)

        main_layout.addWidget(left_frame)
        main_layout.addWidget(text_frame)
        main_layout.addWidget(right_frame)
        

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        # Etiqueta para mensajes
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: green; background-color: #2C2C34;")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el texto
        text_layout.addWidget(self.message_label)  # Agregar al layout
        
    def save_text(self):
        self.text_storage = self.reconocer_texto()
        try:
            resultado = self.comp.separador(self.text_storage)
            if resultado:
                instrucciones_raw, operandos_raw = resultado
                for i in range(len(instrucciones_raw)):
                    instruccion = self.comp.tipoinstruccion(instrucciones_raw[i])
                    operandos = self.comp.convertir_comaflotante(operandos_raw[i])
                    self.instrucciones_procesadas.append(instruccion + operandos[0] + operandos[1])
                    
                # Actualizar memoria de programa y luego inicializar eventos
                self.update_label_memory(self.instrucciones_procesadas, callback=self.initialize_events)

                self.message_label.setText("Texto procesado correctamente.")
                self.message_label.setStyleSheet("color: green;")
            else:
                self.message_label.setText("Error al procesar el texto. Verifica la entrada.")
                self.message_label.setStyleSheet("color: red;")
        except Exception as e:
            print(f"Error: {e}")
            self.message_label.setText(f"Error al procesar: {e}")
            self.message_label.setStyleSheet("color: red;")
    def next_text(self):
        self.text_storage = self.reconocer_texto()
        try:
            resultado = self.comp.separador(self.text_storage)
            mp=self.mp.size()
            if resultado and mp !=0:
                self.mp.clear()
                self.borrar_interfaz()
                self.control_unit.reset()   
                instrucciones_raw, operandos_raw = resultado
                instrucciones_procesadas = []
                for i in range(len(instrucciones_raw)):
                    instruccion = self.comp.tipoinstruccion(instrucciones_raw[i])
                    operandos = self.comp.convertir_comaflotante(operandos_raw[i])
                    instrucciones_procesadas.append(instruccion + operandos[0] + operandos[1])

                # Actualizar memoria de programa y luego inicializar eventos
                self.update_label_memory(instrucciones_procesadas, callback=self.initialize_events)

                self.message_label.setText("Texto procesado correctamente.")
                self.message_label.setStyleSheet("color: green;")
            else:
                self.message_label.setText("No habia texto anterior utiliza el boton guardar texto")
                self.message_label.setStyleSheet("color: red;")
        except Exception as e:
            print(f"Error: {e}")
            self.message_label.setText(f"Error al procesar: {e}")
            self.message_label.setStyleSheet("color: red;")
    def initialize_events(self):
            """
            Inicializa los eventos de `ControlUnit` después de cargar la memoria.
            """
            #try:
            for i, instruccion in enumerate(self.instrucciones_procesadas):
                self.mp.write(number_to_binary(i, 28), instruccion)
            EventBus.set_debug(True)
            self.control_unit.run(mode=ControlUnitMode.RUN, delay=0.5)
            self.imprimir_eventos()
            #except Exception as e:
                #print(f"Error al inicializar CPU: {e}")
                #self.message_label.setText(f"Error al inicializar CPU: {e}")
                #self.message_label.setStyleSheet("color: red;")
    def reconocer_texto(self):
            """
            Procesa el texto del cuadro de texto y lo carga en memoria,
            actualizando primero las etiquetas antes de inicializar los eventos.
            """
            raw_text = self.text_box.toPlainText().strip()
            if not raw_text:
                self.message_label.setText("El cuadro de texto está vacío.")
                self.message_label.setStyleSheet("color: red;")
                return

            self.text_storage = raw_text.splitlines()
            return self.text_storage
    
    def update_label_memory(self, memory, callback=None):
        """
        Actualiza las QLabels de memoria de programa de forma progresiva.
        Una vez completada, ejecuta el callback si está definido.
        """
        if not memory:
            if callback:
                callback()
            return

        self.memory_index = 0

        def update_label():
            if self.memory_index < len(self.program_memory_labels):
                label = self.program_memory_labels[self.memory_index]
                value = memory[self.memory_index] if self.memory_index < len(memory) else "None"
                label.setText(f"{self.memory_index:02}: {value}")
                self.memory_index += 1
            else:
                # Detener el temporizador y ejecutar el callback
                self.memory_timer.stop()
                if callback:
                    callback()

        # Configurar un QTimer para actualizaciones progresivas
        self.memory_timer = QtCore.QTimer()
        self.memory_timer.timeout.connect(update_label)
        self.memory_timer.start(100)  # Intervalo de 100ms para actualizaciones
    def borrar_interfaz(self):
        self.operando_a.setText("a: none")
        self.operando_b.setText("b: none")
        self.output.setText("output: None")
        self.pc.setText("PC: 0000000000000000000000000000")
        self.mar.setText("MAR: None")
        self.mbr.setText("MBR: None")
        self.ir.setText("IR: None")
        self.alu_label.setText("ALU")
        for i in range(10):
            self.registros_memory_labels[i].setText(f"{i}: None")
        for i in range(6):
            self.program_memory_labels[i].setText(f"{i:02}: None")
        
                
    # Método para registros
    def handle_bus_event(self, metadata):
        if  metadata["command"] == Commands.STORE_VALUE:
            if metadata["type"] == MemoryType.REGISTER:
                address = metadata["address"]
                value = metadata["value"]
                address = int(address, 2)
                self.registros_memory_labels[address].setText(f"{address}: {value}")
            elif metadata["type"] == MemoryType.DATA:
                address = metadata["address"]
                value = metadata["value"]
                address = int(address, 2)
                self.data_memory_labels[address].setText(f"{address}: {value}")
        QCoreApplication.processEvents()
    # Método para registros
    def handle_mar_event(self, metadata):
        value = metadata["value"]
        self.mar.setText(f"MAR: {value}")
        QCoreApplication.processEvents()

    def handle_mbr_event(self, metadata):
        value = metadata["value"]
        self.mbr.setText(f"MBR: {value}")
        QCoreApplication.processEvents()
        QTimer.singleShot(500, lambda: self.handle_ir_event(metadata))

    def handle_pc_event(self, metadata):
        value = metadata["position"]
        value = number_to_binary(value, 28)
        self.pc.setText(f"PC: {value}")
        QCoreApplication.processEvents()

    def handle_ir_event(self, metadata):
        value = metadata["value"]
        if value!=None:
            self.ir.setText(f"IR: {value}")
        QCoreApplication.processEvents()
    def handle_alu_event(self, metadata):
        operacion = metadata["operation"]
        QTimer.singleShot(500, lambda:self.alu_label.setText(f"ALU: {operacion}") )
        operand_1 = metadata["operand_1"]
        operand_2 = metadata["operand_2"]
        result = metadata["result"]
        QTimer.singleShot(500, lambda:self.operando_a.setText(f"a: {operand_1}"))
        QTimer.singleShot(500, lambda:self.operando_b.setText(f"b: {operand_2}"))
        QTimer.singleShot(500, lambda:self.output.setText(f"output: {result}"))
        QCoreApplication.processEvents()
    def crear_lista_eventos(self, change: ResourceChange):
        lista = []
        lista.append(change.resource_type)
        lista.append(change.metadata)    
        self.text_storage.append(lista)
    def imprimir_eventos(self):
        print("Imprimiendo eventos")
        for i in range(len(self.text_storage)):
            time.sleep(0.5)
            if self.text_storage[i][0] == ResourceType.MAR:
                self.handle_mar_event(self.text_storage[i][1])
            elif self.text_storage[i][0] == ResourceType.MBR:
                self.handle_mbr_event(self.text_storage[i][1])
            elif self.text_storage[i][0] == ResourceType.PC:
                self.handle_pc_event(self.text_storage[i][1])
            elif self.text_storage[i][0] == ResourceType.ALU:
                self.handle_alu_event(self.text_storage[i][1])
            elif self.text_storage[i][0] == ResourceType.BUS:
                self.handle_bus_event(self.text_storage[i][1])
            else:
                print("Error")          