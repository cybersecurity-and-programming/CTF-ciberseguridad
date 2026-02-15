#!/usr/bin/python3
from pwn import process, remote, xor
from argparse import ArgumentParser
import sys, re

def send_message(objetivo, pass2:bytes, username:bytes):
    objetivo.sendlineafter(b'key: ', pass2)
    objetivo.sendlineafter(b'Codename: ', username)
    objetivo.recvuntil(b'transmission: ')
    return bytes.fromhex(objetivo.recvline().strip().decode())

def main(ip):
    print(ip)
    if ip == "127.0.0.1":
        objetivo = process(['python3', 'server.py'])
    else:
        host, port = ip.split(':')
        objetivo = remote(host, port)

    pass2 = b'A' * 8
    username = b'B' * 1000

    known = f'Agent {username}, your clearance for Operation Blackout is: '.encode()
    ct1 = send_message(objetivo, pass2, username)

    username = b'B' * 5
    ct2 = send_message(objetivo, pass2, username)
    pt = xor(known, ct1, ct2)

    print(re.search(rb'(HTB{.*})\.', pt).groups(1)[0].decode())

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", "--ip", help="ip objetivo, formato host:port", required=True)
    args = parser.parse_args()
    main(args.ip)


