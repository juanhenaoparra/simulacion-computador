import struct
def number_to_binary(number: int, size: int):
    return bin(number)[2:].zfill(size)


def binary_to_number(binary: str):
    return int(binary, 2)

def interpretar_flotante_a_binario(descripcion: str) -> str:
    """
    Interpreta un número en coma flotante con un formato personalizado:
    1 bit de signo, 7 bits de exponente, y 20 bits de mantisa.
    La entrada es una cadena binaria de 28 bits.
    Devuelve el resultado como una cadena en formato binario IEEE 754.

    Parámetros:
        descripcion (str): Cadena de 28 caracteres ('0' y '1') que representa el número binario.

    Retorna:
        str: Representación binaria del valor decimal como un flotante IEEE 754.
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

    # Convertir el valor decimal a binario en formato IEEE 754
    import struct
    valor_binario = ''.join(f"{b:08b}" for b in struct.pack('!f', valor))

    return valor_binario

def number_coma_flotante(number: int):
    number = float(number)  # Convertir a número si es posible
    binary_32bit = f"{struct.unpack('>I', struct.pack('>f', number))[0]:032b}"

    # Descomponer la representación binaria
    sign = binary_32bit[0]  # 1 bit de signo
    exponent = int(binary_32bit[1:9], 2)  # Exponente original
    mantissa = binary_32bit[9:]  # Mantisa original

    # Ajustar exponente y mantisa al formato personalizado
    bias_custom = 63  # Sesgo para el nuevo formato
    adjusted_exponent = max(0, min((exponent - 127) + bias_custom, 127))
    exponent_custom = f"{adjusted_exponent:07b}"
    mantissa_custom = mantissa[:20]

    # Formar la representación final
    custom_float = sign + exponent_custom + mantissa_custom
    return custom_float
