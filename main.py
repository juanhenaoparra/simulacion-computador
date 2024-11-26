import tkinter as tk
from interfaz.carga_instrucciones import TextStorageApp

def main():
    """
    Función principal que inicializa la ventana principal de la aplicación
    y carga la interfaz de usuario.
    """
    # Crear la ventana principal
    root = tk.Tk()
    app = TextStorageApp(root)
    
    # Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()

if __name__ == "__main__":
    main()
