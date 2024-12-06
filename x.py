from interfaz.prueba_mar import TextStorageApp
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
if __name__ == "__main__":
    main()