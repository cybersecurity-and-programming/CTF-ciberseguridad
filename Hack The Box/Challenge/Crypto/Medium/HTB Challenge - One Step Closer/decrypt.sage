#!/usr/bin/env sage

import requests, sys
from Crypto.Util.number import long_to_bytes
from argparse import ArgumentParser

# ============================================================
#  GCD para polinomios en Z/nZ[x] (n compuesto)
# ============================================================

def poly_gcd_composite(f, g):
    """
    Implementacion recursiva del gcd de polinomios sobre Zmod(n),
    porque Sage no lo soporta directamente cuando n no es primo.
    """
    if g == 0:
        return f.monic()
    return poly_gcd_composite(g, f % g)


# ============================================================
#  Ataque Franklin-Reiter
# ============================================================

def franklin_reiter(n, e, ct1, ct2, a1, a2, b1, b2):
    """
    Recupera el mensaje M tal que:
        m1 = a1*M + b1
        m2 = a2*M + b2
    y
        ct1 = m1^e mod n
        ct2 = m2^e mod n
    """

    P.<x> = PolynomialRing(Zmod(n))

    f = (a1 * x + b1)^e - ct1
    g = (a2 * x + b2)^e - ct2

    h = poly_gcd_composite(f, g)

    # h(x) = x + k   donde k ≡ -M mod n
    k = h.coefficients()[0]
    M = (-k) % n

    return int(M)

"""
# ============================================================
#  Conversionn segura de entero ? bytes
# ============================================================

def int_to_bytes_safe(m):
    '''
    Convierte un entero a bytes sin perder ceros iniciales.
    '''
    hex_m = format(m, 'x')
    if len(hex_m) % 2 == 1:
        hex_m = '0' + hex_m
    return bytes.fromhex(hex_m)
"""

# ============================================================
#  Cliente del servidor del reto
# ============================================================

def get_encryption(host):
    """
    Llama al endpoint /api/get_flag y devuelve los parametros parseados.
    """
    r = requests.get(f"http://{host}/api/get_flag")
    data = r.json()

    return {
        "ct": int(data["ct"], 16),
        "n": int(data["n"], 16),
        "e": int(data["e"], 16),
        "a": int(data["a"], 16),
        "b": int(data["b"], 16),
    }


# ============================================================
#  MAIN
# ============================================================

def exploit(host):
    print("[+] Obteniendo primera encriptación…")
    enc1 = get_encryption(host)

    print("[+] Obteniendo segunda encriptación…")
    enc2 = get_encryption(host)

    # n y e son constantes, así que tomamos los de la primera llamada
    n = enc1["n"]
    e = enc1["e"]

    print(f"[+] Ejecutando ataque Franklin–Reiter --> (e={enc1['e']})...")
    M = franklin_reiter(
        n, e,
        enc1["ct"], enc2["ct"],
        enc1["a"], enc2["a"],
        enc1["b"], enc2["b"]
    )

    print("[+] Recuperando flag…")

    #flag = int_to_bytes_safe(M)
    flag = long_to_bytes(M)

    print(f"\n[+] RESULTADO: {flag.decode(errors='ignore')}")
    #print("[+] FLAG =", flag.decode(errors="ignore"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--ip", help="sistema objetivo, ejemplo --> 127.0.0.1:1337", required=True)

    args = parser.parse_args()

    exploit(args.ip)

