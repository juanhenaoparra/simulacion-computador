class Codods:
    def __init__(self):
        self.codods = []
    def tipoinstruccion(tipo):
        if tipo == "ADD":
            return "0000"
        elif tipo == "SUB":
            return "0001"
        elif tipo == "MUL":
            return "0010"
        elif tipo == "DIV":
            return "0011"
        elif tipo == "MOVE":
            return "0100"
        elif tipo == "SAVE":
            return "0101"
        elif tipo == "LOAD":
            return "0110"
        elif tipo == "JUMP":
            return "0111"
        else:
            return "instruccion no valida"

#montar las instrucciones faltantes