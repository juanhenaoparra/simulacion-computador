import struct

class Codificador:
    @staticmethod
    def decimal_to_custom_float_format(data):
        """
        Convierte un array de números decimales o cadenas a un formato de coma flotante personalizado.

        Formato:
        - 1 bit de signo, 7 bits de exponente, 20 bits de mantisa.
        - Prefijos personalizados: '01', '10', '00' según el elemento.

        Parámetros:
        - data (list): Lista de números o cadenas a convertir.

        Retorna:
        - list: Lista de representaciones binarias en el formato personalizado.
        """
        def get_prefix(character):
            """Determina el prefijo según el formato del elemento."""
            if character.startswith('R'):
                return '01'
            elif character.startswith('['):
                return '10'
            elif character[0].isdigit():
                return '00'
            else:
                raise ValueError(f"Caracter no válido para determinar el prefijo: {character}")

        def clean_element(element):
            """Elimina 'R' al inicio y corchetes alrededor del elemento."""
            if element.startswith('R'):
                element = element[1:]  # Eliminar la 'R' al principio
            if element.startswith('[') and element.endswith(']'):
                element = element[1:-1]  # Eliminar corchetes
            return element

        results = []

        for element in data:
            prefix = get_prefix(element)  # Determinar prefijo inicial
            # Limpiar el elemento de 'R' y corchetes
            cleaned_element = clean_element(str(element))

            # Verificar si el elemento estaba entre corchetes y contiene una 'R'
            if element != cleaned_element and 'R' in cleaned_element:
                print(f"Elemento con 'R' encontrado dentro de corchetes, procesando de nuevo: {cleaned_element}")
                # Llamar de nuevo al método para procesar el elemento dentro de los corchetes
                return Codificador.decimal_to_custom_float_format([cleaned_element])  # Recursión

            try:
                number = float(cleaned_element)  # Convertir a número si es posible
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
                custom_float = prefix + sign + exponent_custom + mantissa_custom
                results.append(custom_float)
            except ValueError:
                raise ValueError(f"Elemento no numérico o inválido: {element}")

        return results
