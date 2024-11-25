import re
from compilador.coma_flotante import Codificador
from compilador.codods import Codods

class Compilador:
    def __init__(self):
        self.codods = []

    def tipoinstruccion(self, tipo):
        return Codods.tipoinstruccion(tipo)

    def convertir_comaflotante(flag, numero):
        return Codificador.decimal_to_custom_float_format(flag, numero)

    def separador(array):
        # Expresión regular para validar líneas
        pattern = re.compile(r"^([A-Z]+)\s+((?:\w+|\[\w+\])(?:,\s*(?:\w+|\[\w+\]))*)$")
        # Arreglos separados para instrucciones y operandos
        codods = []
        operandos_list = []
        indicadores = []
        instrucciones = []
        for index, line in enumerate(array):
            match = pattern.match(line)
            if not match:
                print(f"Error en la posición {index}: {line}")
                return  # Interrumpir si hay un error

            codods, operandos = match.groups()
            operandos = [op.strip() for op in operandos.split(",")]  # Separar y limpiar operandos

            # Validar número de operandos
            if len(operandos) < 2 or len(operandos) > 3:
                print(f"Error en la posición {index}: Número inválido de operandos ({len(operandos)})")
                return  # Interrumpir si el número de operandos es incorrecto

            # Guardar instrucción y operandos en arreglos
            codods.append(codods)
            operandos_list.append(operandos)

            # Determinar indicador según número de operandos
            indicador = 1 if len(operandos) == 3 else 0
            indicadores.append(indicador)
