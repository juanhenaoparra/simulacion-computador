import struct

class Codificador:
    @staticmethod
    def decimal_to_custom_float_format(flag, number):
        """
        Convierte un número decimal a un formato de coma flotante de 30 o 20 bits.
        - Si `flag` es 0, se convierte a 30 bits.
        - Si `flag` es 1, se convierte a 20 bits.
        
        Parámetros:
        - flag (int): 0 para 30 bits, 1 para 20 bits.
        - number (float): El número decimal a convertir.

        Retorna:
        - str: Representación binaria del número en formato de 30 o 20 bits.
        """
        
        # Convertir el número decimal a representación IEEE 754 de 32 bits
        binary_32bit = f"{struct.unpack('>I', struct.pack('>f', number))[0]:032b}"
        
        # Separar el bit de signo, exponente y mantisa
        sign = binary_32bit[0]              # 1 bit de signo
        exponent = int(binary_32bit[1:9], 2)  # Exponente original de 8 bits
        mantissa = binary_32bit[9:]         # Mantisa original de 23 bits
        
        # Sesgos para los formatos personalizados
        bias_30bit = 63     # 2^(7-1) - 1
        bias_20bit = 7      # 2^(4-1) - 1
        exponent_bias = 127  # Sesgo original de IEEE 754 de 32 bits

        if flag == 0:  # Convertir a 30 bits
            # Ajustar el exponente para 30 bits
            adjusted_exponent = max(0, min((exponent - exponent_bias) + bias_30bit, 127))
            exponent_30bit = f"{adjusted_exponent:07b}"  # Exponente de 7 bits
            mantissa_30bit = mantissa[:22]               # Mantisa de 22 bits

            # Formar la representación de 30 bits
            custom_30bit = sign + exponent_30bit + mantissa_30bit
            return custom_30bit

        elif flag == 1:  # Convertir a 20 bits
            # Ajustar el exponente para 20 bits
            adjusted_exponent = max(0, min((exponent - exponent_bias) + bias_20bit, 15))
            exponent_20bit = f"{adjusted_exponent:04b}"  # Exponente de 4 bits
            mantissa_20bit = mantissa[:15]               # Mantisa de 15 bits

            # Formar la representación de 20 bits
            custom_20bit = sign + exponent_20bit + mantissa_20bit
            return custom_20bit

        else:
            raise ValueError("Flag inválido. Usa 0 para 30 bits o 1 para 20 bits.")





