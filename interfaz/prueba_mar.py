from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QApplication, QWidget, QGridLayout, QTextEdit, QPushButton
)
from PyQt5.QtCore import QObject, pyqtSignal, QThread, Qt, QCoreApplication
from PyQt5 import QtCore
from cpu.models.events import EventBus, ResourceChange, ResourceType
from compilador.compilador import Compilador
from cpu.control_unit.control_unit import ControlUnit, ControlUnitMode
from cpu.memory.memory import Memory, MemoryType
from cpu.models.events import EventBus, ResourceChange, ResourceType
from cpu.models.directions import number_to_binary
import collections


class EventProcessor(QObject):
    mar_updated = pyqtSignal(str)  # Señal para notificar cambios de MAR

    def __init__(self):
        super().__init__()
        self.mar_changes = collections.deque()  # Buffer para cambios de MAR
        EventBus.subscribe(
            ResourceType.MAR,
            self.handle_mar_event,
            lambda change: change.event == "set_value",
        )

    def handle_mar_event(self, change: ResourceChange):
        """Recibe el cambio en MAR y guarda el valor en el buffer."""
        print("MAR event received")
        value = change.metadata["value"]
        
        # Guardar el valor en el buffer
        self.mar_changes.append(value)
        
        # Emitir la señal para actualizar la interfaz en el hilo principal
        self.mar_updated.emit(value)


class TextStorageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Computer")
        self.setGeometry(100, 100, 800, 500)
        self.init_ui()

        # Inicializar el procesador de eventos en un hilo secundario
        self.event_processor = EventProcessor()
        self.event_thread = QThread()
        self.event_processor.moveToThread(self.event_thread)
        self.event_thread.start()

        # Conectar la señal de mar_updated a un método para actualizar la interfaz
        self.event_processor.mar_updated.connect(self.update_mar_label)

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left Frame
        left_frame = QFrame()
        left_frame.setStyleSheet("background-color: #141414;")
        left_layout = QVBoxLayout()
        left_frame.setLayout(left_layout)

        # Crear QLabel para MAR
        self.mar = QLabel("MAR: None")
        self.mar.setStyleSheet("background-color: #6CCFF6; color: black;")
        self.mar.setFixedWidth(400)
        left_layout.addWidget(self.mar)

        central_widget = QFrame()
        central_widget.setLayout(main_layout)
        main_layout.addWidget(left_frame)
        self.setCentralWidget(central_widget)

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
        self.data_memory_labels = []
        for i in range(10):
            label = QLabel(f"{i}: None")
            label.setStyleSheet("background-color: #C8FFFF; padding: 5px;")
            data_memory_layout.addWidget(label, i // 2, i % 2)
            self.data_memory_labels.append(label)
        right_layout.addWidget(data_memory_frame)

        # Program Memory
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
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar el texto
        text_layout.addWidget(self.message_label)  # Agregar al layout
        
    def save_text(self):
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

                # Actualizar memoria de programa y luego inicializar eventos
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
    def update_mar_label(self, value: str):
        """Actualiza el QLabel de MAR con el nuevo valor."""
        self.mar.setText(f"MAR: {value}")

    def closeEvent(self, event):
        """Cierra el hilo secundario al cerrar la aplicación."""
        self.event_thread.quit()
        self.event_thread.wait()
        super().closeEvent(event)