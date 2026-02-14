import socket, sys, signal
from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_NONE, DCERPCException
from impacket.dcerpc.v5.dcomrt import IObjectExporter
from argparse import ArgumentParser

def exit_handler(sig, frame):
    print("\n[!] Saliendo de la aplicacion...")
    sys.exit(1)

#evento para controlar la salida de la aplicacion con Ctrl+C
signal.signal(signal.SIGINT, exit_handler)

def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--ip", help="comando a ejecutar", required=True)
    args = parser.parse_args()

    target = f'ncacn_ip_tcp:{args.ip}'

    try:
        rpc = transport.DCERPCTransportFactory(target)
        rpc.set_connect_timeout(5)
        dce = rpc.get_dce_rpc()
        dce.set_auth_level(RPC_C_AUTHN_LEVEL_NONE)

        # ---------------------------
        # BLOQUE 1: Conexión RPC
        # ---------------------------
        try:
            dce.connect()
        except socket.timeout:
            print("[!] Timeout al conectar con el servidor RPC")
            return
        except socket.gaierror as e:
            print(f"[!] Error de resolución DNS: {e}")
            return
        except ConnectionRefusedError:
            print("[!] Conexión rechazada por el servidor")
            return
        except OSError as e:
            print(f"[!] Error OS al conectar: {e}")
            return
        except BaseException as e:
            print(f"[!] Error inesperado en la conexión RPC ({type(e).__name__}): {e}")
            return

        # ---------------------------
        # BLOQUE 2: Llamada ServerAlive2
        # ---------------------------
        try:
            obj = IObjectExporter(dce)
            bindings = obj.ServerAlive2()
        except DCERPCException as e:
            print(f"[!] Error DCERPC ejecutando ServerAlive2: {e}")
            return
        except RuntimeError as e:
            print(f"[!] Error de ejecución en ServerAlive2: {e}")
            return
        except OSError as e:
            print(f"[!] Error OS en ServerAlive2: {e}")
            return
        except BaseException as e:
            print(f"[!] Error inesperado en ServerAlive2 ({type(e).__name__}): {e}")
            return

        # ---------------------------
        # BLOQUE 3: Procesar bindings
        # ---------------------------
        for b in bindings:
            try:
                fields = b.fields  # diccionario interno real

                proto = b['aProtocol'] if 'aProtocol' in fields else None
                addr = b['aNetworkAddr'] if 'aNetworkAddr' in fields else None
                endpoint = b['aEndpoint'] if 'aEndpoint' in fields else None

                print(f"Proto: {proto} | Addr: {addr} | Endpoint: {endpoint}")
            except KeyError as e:
                print(f"[!] Falta una clave en el binding: {e}")
                print("    Raw:", repr(b))
            except TypeError as e:
                print(f"[!] Tipo inesperado en binding: {e}")
                print("    Raw:", repr(b))
            except ValueError as e:
                print(f"[!] Valor inválido en binding: {e}")
                print("    Raw:", repr(b))
            except BaseException as e:
                print(f"[!] Error inesperado procesando binding ({type(e).__name__}): {e}")
                print("    Raw:", repr(b))

    # ---------------------------
    # BLOQUE 4: Errores globales
    # ---------------------------
    except OSError as e:
        print(f"[!] Error OS general: {e}")

    except BaseException as e:
        print(f"[!] Error inesperado general ({type(e).__name__}): {e}")

if __name__ == "__main__":
    main()
