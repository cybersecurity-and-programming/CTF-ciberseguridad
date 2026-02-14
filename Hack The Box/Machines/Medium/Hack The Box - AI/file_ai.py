#!/usr/bin/env python3
import sys
import requests
import re
import subprocess


def create_file(query: str) -> None:
    """
    Convierte la consulta de texto a audio utilizando text2wave.
    Se realizan sustituciones para evitar problemas con ciertos caracteres.
    El archivo resultante se guarda en 'ai.wav'.
    """
    # Reemplazos de caracteres problemáticos. Ajusta según sea necesario.
    query = query.replace("'", " open single quote ").replace("#", " Pound sign ")
    
    try:
        # Ejecuta text2wave pasándole la consulta por STDIN.
        subprocess.run(
            ["text2wave", "-o", "ai.wav"],
            input=query.encode(),
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error al generar el archivo de audio: {e}", file=sys.stderr)
        sys.exit(1)

def send_file(url: str, file_path: str, proxies: dict = None) -> str:
    """
    Envía el archivo de audio al servidor especificado y retorna la respuesta.
    """
    try:
        with open(file_path, "rb") as file:
            files = {
                "fileToUpload": file,
                "submit": (None, "Process It!")
            }
            response = requests.post(url, files=files, proxies=proxies)
            response.raise_for_status()  # Verifica que la petición haya sido exitosa.
            return response.text
    except Exception as e:
        print(f"Error al enviar el archivo: {e}", file=sys.stderr)
        sys.exit(1)

def parse_response(response_text: str) -> tuple:
    """
    Extrae y retorna la interpretación de la consulta y el resultado usando expresiones regulares.
    """
    query_match = re.search(r"Our understanding of your input is\s*:\s*(.*)<br\s*/?>", response_text)
    result_match = re.search(r"Query result\s*:\s*(.*)<h3>", response_text)
    
    interpretacion = query_match.group(1).strip() if query_match else "No se pudo interpretar la consulta."
    resultado = result_match.group(1).strip() if result_match else "No se obtuvo resultado."
    return interpretacion, resultado

def main():
    url = "http://10.129.17.46/ai.php"
    # Configura el proxy si es necesario
    # proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    proxies = None
    
    while True:
        try:
            query = input("Enter query> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            sys.exit(0)
            
        if query.lower() == 'exit':
            sys.exit()
            
        if not query:
            print("Por favor, ingresa una consulta válida.")
            continue

        create_file(query)
        response_text = send_file(url, "ai.wav", proxies)
        interpretacion, resultado = parse_response(response_text)
        
        print("Query:", interpretacion)
        print("Result:", resultado)

if __name__ == "__main__":
    main()

