import re
from compilador.coma_flotante import Codificador
from compilador.codods import Codods

class Compilador:
    def __init__(self):
        self.codods = []

    def tipoinstruccion(self, tipo):
        """Obtiene el código binario de una instrucción a partir de su tipo."""
        binario=Codods.tipoinstruccion(tipo)
        return binario

    @staticmethod
    def convertir_comaflotante(data):
        """Convierte datos a un formato de coma flotante personalizado."""
        ComaFlotante= Codificador.decimal_to_custom_float_format(data)
        return ComaFlotante

    def separador(self, array):
        """
        Separa las instrucciones y sus operandos de un arreglo de cadenas.

        Parámetros:
        - array (list): Lista de cadenas con instrucciones y operandos.

        Retorna:
        - tuple: (lista de instrucciones, lista de operandos).

        Si hay un error en la validación, imprime el error y retorna None.
        """
        pattern = re.compile(r"^([A-Z]+)\s+((?:\w+|\[\w+\])(?:,\s*(?:\w+|\[\w+\]))*)$")
        instrucciones = []
        operandos_list = []

        for index, line in enumerate(array):
            match = pattern.match(line)
            if not match:
                print(f"Error en la posición {index}: {line}")
                return None  # Interrumpir si hay un error

            instruccion, operandos = match.groups()
            operandos = [op.strip() for op in operandos.split(",")]  # Separar y limpiar operandos

            # Validar número de operandos
            if len(operandos) < 2 or len(operandos) > 3:
                print(f"Error en la posición {index}: Número inválido de operandos ({len(operandos)})")
                return None  # Interrumpir si el número de operandos es incorrecto

            # Guardar instrucción y operandos en listas
            instrucciones.append(instruccion)
            operandos_list.append(operandos)

        return instrucciones, operandos_list
