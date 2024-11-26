import tkinter as tk
from compilador.compilador import Compilador
from cpu.control_unit.control_unit import ControlUnit, ControlUnitMode
from cpu.memory.memory import Memory, MemoryType
from cpu.memory.register import Register
from cpu.models.events import EventBus
from cpu.models.directions import number_to_binary


class TextStorageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz de Texto")

        # Crear un cuadro de texto
        self.text_box = tk.Text(root, width=40, height=10, bg="white", fg="black")
        self.text_box.pack(pady=10)

        # Botón para guardar el texto
        self.save_button = tk.Button(root, text="Guardar Texto", command=self.save_text)
        self.save_button.pack(pady=5)

        # Etiqueta para mostrar mensajes
        self.message_label = tk.Label(root, text="", fg="green")
        self.message_label.pack(pady=5)

        # Objeto para almacenar el texto
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
                for i in range(0, len(instrucciones_raw)):
                    instruccion = comp.tipoinstruccion(instrucciones_raw[i])
                    operandos = comp.convertir_comaflotante(operandos_raw[i])
                    instrucciones_procesadas.append(
                        instruccion + operandos[0] + operandos[1]
                    )

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
            print("instrucciones a procesar: ", instrucciones_procesadas)
            mp = Memory(MemoryType.PROGRAM)
            for i in range(0, len(instrucciones_procesadas)):
                mp.write(number_to_binary(i, 28), instrucciones_procesadas[i])

            md = Memory(MemoryType.DATA)
            md.write(number_to_binary(1, 28), number_to_binary(10, 64))
            md.write(number_to_binary(2, 28), number_to_binary(20, 64))
            md.write(number_to_binary(3, 28), number_to_binary(30, 64))
            md.write(number_to_binary(4, 28), number_to_binary(40, 64))

            mr = Register()
            mr.write(number_to_binary(1, 28), number_to_binary(100, 64))
            mr.write(number_to_binary(2, 28), number_to_binary(200, 64))

            EventBus.set_debug(False)

            control_unit = ControlUnit()
            control_unit.run(mode=ControlUnitMode.RUN, delay=1)
        except Exception as e:
            print(f"Error al inicializar CPU: {e}")
            self.message_label.config(text=f"Error al inicializar CPU: {e}", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = TextStorageApp(root)
    root.mainloop()
