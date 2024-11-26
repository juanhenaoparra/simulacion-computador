def number_to_binary(number: int, size: int):
    return bin(number)[2:].zfill(size)


def binary_to_number(binary: str):
    return int(binary, 2)
