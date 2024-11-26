import tkinter as tk
from compilador.compilador import Compilador

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
                instrucciones, operandos = resultado

                # Procesar y mostrar la primera instrucción y su primer operando
                primera_instruccion = comp.tipoinstruccion(instrucciones[0])
                primer_operando = comp.convertir_comaflotante([operandos[0][0]])[0]

                print(f"Primera instrucción: {primera_instruccion}")
                print(f"Primer operando: {primer_operando}")
                print(f"Instrucciones: {instrucciones}")
                print(f"Operandos: {operandos}")

                self.message_label.config(text="Texto procesado correctamente.", fg="green")
            else:
                self.message_label.config(text="Error al procesar el texto. Verifica la entrada.", fg="red")
        except Exception as e:
            print(f"Error: {e}")
            self.message_label.config(text=f"Error al procesar: {e}", fg="red")

        # Mostrar el texto guardado en la consola
        print(f"Texto guardado: {self.text_storage}")

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = TextStorageApp(root)
    root.mainloop()
