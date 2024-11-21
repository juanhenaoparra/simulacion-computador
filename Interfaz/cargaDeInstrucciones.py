import tkinter as tk

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

        # Objeto para guardar el texto
        self.text_storage = ""
        
    def save_text(self):
        # Guardar cada línea del cuadro de texto en un array (lista)
        self.text_storage = self.text_box.get("1.0", tk.END).strip().splitlines()
        print(f"Texto guardado: {self.text_storage}")  # Muestra el texto guardado en la consola

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = TextStorageApp(root)
    root.mainloop()
