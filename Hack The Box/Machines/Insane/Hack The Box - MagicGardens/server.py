#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json,signal,sys

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Enviar respuesta exitosa
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Leer el contenido de la solicitud
            length = int(self.headers.get('Content-Length', 0))
            message = json.loads(self.rfile.read(length))

            # Validar los datos recibidos (opcional, dependiendo del contexto)
            if not all(key in message for key in ('cardnumber', 'cardname')):
                response = {"status": "400", "message": "Bad Request: Missing required fields"}
            else:
                # Construir el mensaje de respuesta
                response = {
                    "status": "200",
                    "message": "OK",
                    "cardnumber": message["cardnumber"],
                    "cardname": message["cardname"]
                }

            # Convertir el mensaje a JSON
            response_json = json.dumps(response).encode()
            
            # Escribir la respuesta
            self.wfile.write(response_json)

        except json.JSONDecodeError:
            # Manejo de errores para JSON inválido
            error_message = json.dumps({"status": "400", "message": "Bad Request: Invalid JSON"}).encode()
            self.wfile.write(error_message)

        except Exception as e:
            # Manejo de errores generales
            error_message = json.dumps({"status": "500", "message": f"Internal Server Error: {e}"}).encode()
            self.wfile.write(error_message)

def exit_handler(sig, frame):
	print("\n[!] Saliendo de la aplicacion...")
	sys.exit(1)
	
#evento para controlar la salida de la aplicacion con Ctrl+C
signal.signal(signal.SIGINT, exit_handler)

if __name__ == "__main__":
    with HTTPServer(('', 80), Handler) as server:
        print("Servidor corriendo en el puerto 80...")
        server.serve_forever()

