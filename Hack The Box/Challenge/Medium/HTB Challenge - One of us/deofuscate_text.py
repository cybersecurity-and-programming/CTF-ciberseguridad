#!/usr/bin/env python
from rijndael.cipher.crypt import new
from rijndael.cipher.blockcipher import MODE_CBC
import base64
import binascii
import sys

# Clave estática conocida.
KEY = "8xppg2oX68Bo6koL7hwSeC8bCEWvk540"   # 32 bytes ASCII

# Tamaño de bloque de Rijndael-256. Importante para validar IV y padding.
BLOCKSIZE = 32


def extract_iv_and_ciphertext(path):
    """
    Extrae la línea que contiene IV|CipherText desde un archivo de evidencia.
    En análisis forense, se asume que el archivo proviene de una adquisición
    íntegra y se debe registrar su hash antes de procesarlo.
    """
    with open(path) as f:
        for line in f:
            if "|" in line:
                parts = line.strip().split("|", 1)

                # Validación estricta: evita falsos positivos o líneas corruptas.
                if len(parts) != 2:
                    raise ValueError("La línea con '|' no tiene el formato esperado.")

                iv, ct = parts
                return iv.strip(), ct.strip()

    # Si no se encuentra, se documenta como evidencia incompleta o manipulada.
    raise ValueError("No se encontró ninguna línea con IV|CipherText en el archivo.")


def validate_ascii_length(name, value, expected_len):
    """
    Valida que un campo crítico (clave o IV) tenga la longitud exacta.
    En un análisis forense, esto ayuda a detectar corrupción, truncamiento
    o manipulación intencionada del material cifrado.
    """
    if len(value) != expected_len:
        raise ValueError(
            "%s debe tener exactamente %d bytes ASCII, pero tiene %d." %
            (name, expected_len, len(value))
        )


def decode_ciphertext_b64(ct_b64):
    """
    Decodifica Base64 con validación explícita.
    En un entorno forense, errores aquí pueden indicar:
    - Corrupción del archivo
    - Manipulación deliberada
    - Codificación no estándar
    """
    try:
        return base64.b64decode(ct_b64)
    except (TypeError, binascii.Error):
        raise ValueError("El CipherText no es Base64 válido.")


def decrypt_rijndael256(key, iv, ciphertext):
    """
    Descifra Rijndael-256 CBC.
    Desde la perspectiva forense, es importante:
    - Registrar la herramienta y versión usada para descifrado
    - Mantener reproducibilidad del proceso
    - Documentar si el padding es válido o no (posible indicador de manipulación)
    """
    cipher = new(key, MODE_CBC, iv, blocksize=BLOCKSIZE)
    plaintext_padded = cipher.decrypt(ciphertext)

    # Validación de padding PKCS7
    last_byte = ord(plaintext_padded[-1])
    if 1 <= last_byte <= BLOCKSIZE:
        if plaintext_padded.endswith(chr(last_byte) * last_byte):
            return plaintext_padded[:-last_byte]

    # Si el padding no es válido, se devuelve el contenido completo.
    return plaintext_padded


def main():
    # Extracción del IV y ciphertext desde la evidencia.
    try:
        iv, ct_b64 = extract_iv_and_ciphertext("mail.txt")
    except ValueError as e:
        print("Error al extraer IV y CipherText:", e)
        sys.exit(1)

    # Validación estructural de clave e IV.
    try:
        validate_ascii_length("La clave", KEY, 32)
        validate_ascii_length("El IV", iv, 32)
    except ValueError as e:
        print("Error de validación:", e)
        sys.exit(1)

    # Decodificación segura del ciphertext.
    try:
        ciphertext = decode_ciphertext_b64(ct_b64)
    except ValueError as e:
        print("Error al decodificar Base64:", e)
        sys.exit(1)

    # Descifrado y recuperación del texto.
    plaintext = decrypt_rijndael256(KEY, iv, ciphertext)

    print("\n=== TEXTO LIMPIO ===")
    print(plaintext.replace("\x00", ""))


if __name__ == "__main__":
    main()
