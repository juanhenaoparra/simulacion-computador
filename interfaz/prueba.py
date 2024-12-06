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

        # Configuración del layout principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def handle_event(self, updater):
        """
        Genera un manejador de eventos para cada registro.
        """
        def event_handler(change: ResourceChange):
            value = change.metadata.get("value")
            updater.update_signal.emit(value)

        return event_handler

    # Métodos para actualizar etiquetas desde señales
    def update_mar_label(self, value):
        self.mar.setText(f"MAR: {value}")

    def update_mbr_label(self, value):
        self.mbr.setText(f"MBR: {value}")

    def update_pc_label(self, value):
        self.pc.setText(f"PC: {value}")

    def update_ir_label(self, value):
        self.ir.setText(f"IR: {value}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextStorageApp()
    window.show()
    sys.exit(app.exec_())
