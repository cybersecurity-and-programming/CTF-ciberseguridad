#!/usr/bin/python3
import ctypes

PASSWORD_LENGTH = 20
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
CHARSET_SIZE = len(CHARSET)

# Cargar libc para usar srand/rand de C
libc = ctypes.CDLL("libc.so.6")

def generate_password(seed: int) -> str:
    libc.srand(seed)
    chars = [CHARSET[libc.rand() % CHARSET_SIZE] for _ in range(PASSWORD_LENGTH)]
    return "".join(chars)

def generate_all_passwords(timestamp: int, count: int = 1000) -> list[str]:
    seen = set()
    passwords = []
    for ms in range(count):
        seed = timestamp * 1000 + ms
        password = generate_password(seed)
        if password not in seen:
            seen.add(password)
            passwords.append(password)
    return passwords

def main():
    # Timestamp fijo: 2024-08-30 14:40:42 = 1725028842
    timestamp_sec = 1725028842
    passwords = generate_all_passwords(timestamp_sec)
    for i, pwd in enumerate(passwords, 1):
        print(f"{i:04d}: {pwd}")

if __name__ == "__main__":
    main()
