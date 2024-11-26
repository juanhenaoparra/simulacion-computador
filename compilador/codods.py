class Codods:
    @staticmethod
    def tipoinstruccion(tipo):
        """
        Obtiene el código binario correspondiente a una instrucción.

        Parámetros:
        - tipo (str): Nombre de la instrucción.

        Retorna:
        - str: Código binario de 4 bits o mensaje de error.
        """
        instrucciones = {
            "ADD": "0000",
            "SUB": "0001",
            "MUL": "0010",
            "DIV": "0011",
            "MOVE": "0100",
            "SAVE": "0101",
            "LOAD": "0110",
            "JUMP": "0111"
        }
        return instrucciones.get(tipo, "instrucción no válida")
