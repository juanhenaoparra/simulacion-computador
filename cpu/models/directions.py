import struct
def number_to_binary(number: int, size: int):
    return bin(number)[2:].zfill(size)


def binary_to_number(binary: str):
    return int(binary, 2)

def interpretar_flotante_a_decimal(descripcion: str) -> float:
    """
    Interpreta un número en coma flotante con un formato personalizado:
    1 bit de signo, 7 bits de exponente, y 20 bits de mantisa.
    La entrada es una cadena binaria de 28 bits.
    Devuelve el resultado como un número decimal de punto flotante.

    Parámetros:
        descripcion (str): Cadena de 28 caracteres ('0' y '1') que representa el número binario.

    Retorna:
        float: Valor decimal correspondiente al número representado.
    """
    # Validar la entrada
    assert len(descripcion) == 28 and all(c in '01' for c in descripcion), \
        "La descripción debe ser una cadena binaria de 28 bits."

    # Convertir la cadena binaria a un entero
    bits = int(descripcion, 2)

    # Extraer los campos
    signo = (bits >> 27) & 0b1  # El bit más significativo
    exponente = (bits >> 20) & 0b1111111  # Los siguientes 7 bits
    mantisa = bits & 0xFFFFF  # Los últimos 20 bits

    # Convertir el exponente con un bias de 63 (2^(7-1) - 1)
    bias = 63
    exponente_real = exponente - bias

    # Reconstruir el valor real de la mantisa (añadiendo el bit implícito)
    mantisa_real = 1.0 + (mantisa / (1 << 20))  # La mantisa está normalizada

    # Calcular el valor final
    valor = mantisa_real * (2 ** exponente_real)

    # Aplicar el signo
    if signo == 1:
        valor = -valor

    return valor

def number_coma_flotante(number: float) -> str:
    """
    Convierte un número decimal en coma flotante (float) a una representación binaria personalizada:
    1 bit de signo, 7 bits de exponente (con sesgo de 63) y 20 bits de mantisa.

    Parámetros:
        number (float): El número decimal a convertir.

    Retorna:
        str: Representación binaria en formato personalizado (28 bits).
    """
    # Convertir el número a su representación binaria IEEE 754 de 32 bits
    binary_32bit = f"{struct.unpack('>I', struct.pack('>f', number))[0]:032b}"

    # Descomponer la representación binaria IEEE 754
    sign = binary_32bit[0]  # 1 bit de signo
    exponent = int(binary_32bit[1:9], 2)  # Exponente original (8 bits)
    mantissa = binary_32bit[9:]  # Mantisa original (23 bits)

    # Ajustar el exponente al formato personalizado (7 bits con sesgo de 63)
    bias_ieee = 127  # Sesgo del formato IEEE 754
    bias_custom = 63  # Sesgo del formato personalizado
    adjusted_exponent = (exponent - bias_ieee) + bias_custom

    # Validar rango del exponente ajustado para el formato personalizado
    if adjusted_exponent < 0:
        adjusted_exponent = 0  # Subnormal
    elif adjusted_exponent > 127:
        adjusted_exponent = 127  # Saturación máxima

    exponent_custom = f"{adjusted_exponent:07b}"  # 7 bits de exponente ajustado
    mantissa_custom = mantissa[:20]  # Tomar los primeros 20 bits de la mantisa

    # Formar la representación final
    custom_float = sign + exponent_custom + mantissa_custom
    return custom_float