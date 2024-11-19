from ComaFlotante import Codificador
class Codods:
    def __init__(self):
        self.codods = []
    def convertir_comaflotante(self, flag, numero):
        """
        Convierte un número decimal a un formato de coma flotante de 30 o 20 bits.
        - Si `flag` es 0, se convierte a 30 bits.
        - Si `flag` es 1, se convierte a 20 bits.
        
        Parámetros:
        - flag (int): 0 para 30 bits, 1 para 20 bits.
        - numero (float): El número decimal a convertir.

        Retorna:
        - str: Representación binaria del número en formato de 30 o 20 bits.
        """
        return Codificador.decimal_to_custom_float_format(flag, numero)
    
    