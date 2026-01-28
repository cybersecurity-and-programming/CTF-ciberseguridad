#!/usr/bin/python3
import logging
from argparse import ArgumentParser

def xorString(data, length):
    """
    Descifra un payload usando el XOR dinámico original del challenge.
    El XOR key muta en cada iteración según:
        xor_key = ((xor_key ^ 99) ^ (i % 254))
    """
    xor_key = 45
    result = bytearray()

    for i in range(length):
        result.append(data[i] ^ xor_key)
        xor_key = ((xor_key ^ 99) ^ (i % 254))
    return bytes(result)


def regex_file(file_content):
    """
    Devuelve el índice donde empieza el payload.
    """
    pattern = b'sWcDWp36x5oIe2hJGnRy1iC92AcdQgO8RLioVZWlhCKJXHRSqO450AiqLZyLFeXYilCtorg0p3RdaoPa'
    index = file_content.find(pattern)
    return index + len(pattern)

def main(name_file, verbose=False):
    try:
        with open(name_file, 'rb') as archivo:
            contenido = archivo.read()

        index = regex_file(contenido)

        if verbose:
            print(f"[+] Offset encontrado: {index}")
            print(f"[+] Tamaño esperado del payload: {13082} bytes")

        payload_encrypted = contenido[index:index + 13082]
        payload_decrypted = xorString(payload_encrypted, len(payload_encrypted))

        with open("malicious.js", "wb") as out:
            out.write(payload_decrypted)

    except FileNotFoundError:
        logging.error(f"Archivo no encontrado: {name_file}")
    except OSError as e:
        logging.error(f"Error guardando archivo: {e}")
    except Exception as e:
        logging.error(f"Error procesando el archivo: {e}")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="archivo a leer", required=True)
    parser.add_argument("-v", "--verbose", action="store_true", help="mostrar información adicional")
    args = parser.parse_args()

    main(args.file, args.verbose)
