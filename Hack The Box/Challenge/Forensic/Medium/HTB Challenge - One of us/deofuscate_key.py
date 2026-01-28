#!/usr/bin/env python3
import base64

def nkalPYSrDkoirG(in_array, offset):
    """
    Decodifica un array de enteros aplicando XOR contra una clave
    derivada de un bloque base64. Esta función es típica en rutinas
    de desofuscación usadas en malware o scripts empaquetados.

    Parámetros:
        in_array (list[int]): Lista de enteros ya evaluados.
        offset (int): Desplazamiento dentro del byte_list.

    Retorna:
        str: Cadena descifrada.
    """

    # Decodificar la clave base64 una sola vez
    try:
        byte_list = base64.b64decode("eNS7GlezU9snp3ciGjUJ9HD0eo5......")
    except Exception as e:
        raise ValueError("Error al decodificar la clave base64: %s" % e)

    # Validación básica
    if offset < 0 or offset + len(in_array) > len(byte_list):
        raise ValueError("Offset fuera de rango para el tamaño de byte_list.")

    # Construcción eficiente de la cadena
    chars = []
    for i, value in enumerate(in_array):
        decoded = byte_list[i + offset] ^ value
        chars.append(chr(decoded))

    return "".join(chars)

def garbage_to_string(string):

    print(eval(string.replace("Array", "").replace("&", "+")))

if __name__ == "__main__":
    garbage_to_string(
        "nkalPYSrDkoirG(Array((27 ^ 96), (69 ^ 194), 173, (126 + 125), 121, (59 ^ 163), (34 ^ 135), ((35 ^ 6) + 94), 51, ((12 ^ 0) + (87 ^ 9)), (17 + (2 ^ 4)), 231, (20 + (21 ^ 8)), ((0 ^ 3) + 110), 196, (169 + 19), 30, 231, (66 + (7 ^ 106)), (210 ^ 51), (97 + 17), (142 + (5 ^ 26)), (9 + (98 ^ 167)), 191, 220, (31 ^ 205), ((42 ^ 91) + 120), (94 + 0), 135), (51 ^ 371)) & nkalPYSrDkoirG(Array((37 ^ 176), ((6 ^ 47) + 190), 36), ((161 ^ 123) + (40 ^ 171)))"
    )
