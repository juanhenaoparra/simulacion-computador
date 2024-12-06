import tkinter as tk
#from interfaz.carga_instrucciones import TextStorageApp
from interfaz.nueva_interfaz import TextStorageApp
from PyQt5.QtWidgets import (
    QApplication
)


def main():
    """
    Función principal que inicializa la ventana principal de la aplicación
    y carga la interfaz de usuario.
    """
    app = QApplication([])
    window = TextStorageApp()
    window.show()
    app.exec_()
    
    # Crear la ventana principal
    #root = tk.Tk()
    #app = TextStorageApp(root)

    # Iniciar el bucle principal de la interfaz gráfica
    #root.mainloop()


if __name__ == "__main__":
    main()
