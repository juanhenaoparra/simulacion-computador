from PyQt5.QtCore import Qt, QTimer, QCoreApplication, QObject, pyqtSignal
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QWidget, QGridLayout, QFrame, QApplication
)
from compilador.compilador import Compilador
from cpu.control_unit.control_unit import ControlUnit, ControlUnitMode
from cpu.memory.memory import Memory, MemoryType
from cpu.models.events import EventBus, ResourceChange, ResourceType
from cpu.models.directions import number_to_binary
import sys


class RegisterUpdater(QObject):
    """
    Clase que emite señales para actualizar registros.
    """
    update_signal = pyqtSignal(str)


class TextStorageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Computer")
        self.setGeometry(100, 100, 800, 500)

        # Inicialización de actualizadores por registros
        self.mar_updater = RegisterUpdater()
        self.mbr_updater = RegisterUpdater()
        self.pc_updater = RegisterUpdater()
        self.ir_updater = RegisterUpdater()

        # Conectar señales de actualizadores a las etiquetas correspondientes
        self.mar_updater.update_signal.connect(self.update_mar_label)
        self.mbr_updater.update_signal.connect(self.update_mbr_label)
        self.pc_updater.update_signal.connect(self.update_pc_label)
        self.ir_updater.update_signal.connect(self.update_ir_label)

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left Frame
        left_frame = QFrame()
        left_frame.setStyleSheet("background-color: #141414;")
        left_layout = QVBoxLayout()
        left_frame.setLayout(left_layout)

        # Crear etiquetas de registros
        self.pc = QLabel("PC: 00")
        self.pc.setStyleSheet("background-color: #6CCFF6; color: black;")
        self.pc.setFixedWidth(400)
        left_layout.addWidget(self.pc)

        self.mar = QLabel("MAR: None")
        self.mar.setStyleSheet("background-color: #6CCFF6; color: black;")
        self.mar.setFixedWidth(400)
        left_layout.addWidget(self.mar)

        self.mbr = QLabel("MBR: None")
        self.mbr.setStyleSheet("background-color: #6CCFF6; color: black;")
        self.mbr.setFixedWidth(400)
        left_layout.addWidget(self.mbr)

        self.ir = QLabel("IR: None")
        self.ir.setStyleSheet("background-color: #6CCFF6; color: black;")
        self.ir.setFixedWidth(400)
        left_layout.addWidget(self.ir)

        # Suscripción a eventos del EventBus
        EventBus.subscribe(ResourceType.MAR, self.handle_event(self.mar_updater))
        EventBus.subscribe(ResourceType.MBR, self.handle_event(self.mbr_updater))
        EventBus.subscribe(ResourceType.PC, self.handle_event(self.pc_updater))
        EventBus.subscribe(ResourceType.IR, self.handle_event(self.ir_updater))

        # Right Frame
        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: #1C3A40;")
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        # Memoria de datos
        data_memory_layout = QGridLayout()
        data_memory_frame = QFrame()
        data_memory_frame.setStyleSheet("background-color: #32CD32;")
        data_memory_frame.setLayout(data_memory_layout)
        self.data_memory_labels = []
        for i in range(10):
            label = QLabel(f"{i}: None")
            label.setStyleSheet("background-color: #C8FFFF; padding: 5px;")
            data_memory_layout.addWidget(label, i // 2, i % 2)
            self.data_memory_labels.append(label)
        right_layout.addWidget(data_memory_frame)

        # Memoria de programa
        program_memory_layout = QGridLayout()
        program_memory_frame = QFrame()
        program_memory_frame.setStyleSheet("background-color: #32CD32;")
        program_memory_frame.setLayout(program_memory_layout)
        self.program_memory_labels = []
        for i in range(10):
            label = QLabel(f"{i:02}: None")
            label.setStyleSheet("background-color: #C8FFFF; padding: 5px;")
            program_memory_layout.addWidget(label, i // 2, i % 2)
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
        button_layout.addWidget(self.next_button)

        self.load_button = QPushButton("Load")
        button_layout.addWidget(self.load_button)

        text_layout.addLayout(button_layout)

        main_layout.addWidget(left_frame)
        main_layout.addWidget(right_frame)
        main_layout.addWidget(text_frame)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Etiqueta para mensajes
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: green; background-color: #2C2C34;")
        self.message_label.setAlignment(Qt.AlignCenter)  # Centrar el texto
        text_layout.addWidget(self.message_label)  # Agregar al layout

    def save_text(self):
        """
        Procesa el texto del cuadro de texto y lo carga en memoria.
        """
        raw_text = self.text_box.toPlainText().strip()
        if not raw_text:
            self.message_label.setText("El cuadro de texto está vacío.")
            self.message_label.setStyleSheet("color: red;")
            return

        self.text_storage = raw_text.splitlines()
        comp = Compilador()

        try:
            resultado = comp.separador(self.text_storage)
            if resultado:
                instrucciones_raw, operandos_raw = resultado
                instrucciones_procesadas = []
                for i in range(len(instrucciones_raw)):
                    instruccion = comp.tipoinstruccion(instrucciones_raw[i])
                    operandos = comp.convertir_comaflotante(operandos_raw[i])
                    instrucciones_procesadas.append(instruccion + operandos[0] + operandos[1])

                def initialize_events():
                    """
                    Inicializa los eventos de `ControlUnit` después de cargar la memoria.
                    """
                    try:
                        mp = Memory(MemoryType.PROGRAM)
                        for i, instruccion in enumerate(instrucciones_procesadas):
                            mp.write(number_to_binary(i, 28), instruccion)

                        control_unit = ControlUnit()
                        EventBus.set_debug(True)
                        control_unit.run(mode=ControlUnitMode.RUN, delay=1)
                    except Exception as e:
                        print(f"Error al inicializar CPU: {e}")
                        self.message_label.setText(f"Error al inicializar CPU: {e}")
                        self.message_label.setStyleSheet("color: red;")

                self.update_label_memory(instrucciones_procesadas, callback=initialize_events)

                self.message_label.setText("Texto procesado correctamente.")
                self.message_label.setStyleSheet("color: green;")
            else:
                self.message_label.setText("Error al procesar el texto. Verifica la entrada.")
                self.message_label.setStyleSheet("color: red;")
        except Exception as e:
            print(f"Error: {e}")
            self.message_label.setText(f"Error al procesar: {e}")
            self.message_label.setStyleSheet("color: red;")

    def handle_event(self, updater):
        """
        Genera un manejador de eventos para cada registro.
        """
        def event_handler(change: ResourceChange):
            value = change.metadata.get("value")
            updater.update_signal.emit(value)

        return event_handler

    def update_label_memory(self, memory, callback=None):
        """
        Actualiza las etiquetas de memoria progresivamente.
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
                self.memory_timer.stop()
                if callback:
                    callback()

        self.memory_timer = QTimer()
        self.memory_timer.timeout.connect(update_label)
        self.memory_timer.start(100)

    # Métodos para actualizar etiquetas desde señales
    def update_mar_label(self, value):
        self.mar.setText(f"MAR: {value}")

    def update_mbr_label(self, value):
        self.mbr.setText(f"MBR: {value}")

    def update_pc_label(self, value):
        self.pc.setText(f"PC: {value}")

    def update_ir_label(self, value):
        self.ir.setText(f"IR: {value}")

    
