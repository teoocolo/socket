import socket
import json
from threading import Thread

def ricevi_comandi(sock_service, addr_client):
    print(f"--- Inizio sessione con {addr_client} ---")
    try:
        while True:
            data = sock_service.recv(DIM_BUFFER)
            
            if not data:
                break
                
            try:
                messaggio_str = data.decode("UTF-8")
                print(f"Ricevuto messaggio da {addr_client}: {messaggio_str}")
                
                messaggio = json.loads(messaggio_str)
                primoNumero = messaggio["primoNumero"]
                operazione = messaggio["operazione"]
                secondoNumero = messaggio["secondoNumero"]
                
                if operazione == "+":
                    risultato = primoNumero + secondoNumero
                elif operazione == "-":
                    risultato = primoNumero - secondoNumero
                elif operazione == "*":
                    risultato = primoNumero * secondoNumero
                elif operazione == "/":
                    risultato = primoNumero / secondoNumero if secondoNumero != 0 else "Errore: divisione per zero"
                elif operazione == "%":
                    risultato = primoNumero % secondoNumero if secondoNumero != 0 else "Errore: divisione per zero"
                else:
                    risultato = "Errore: operazione non valida"
                
                # Invio risposta
                sock_service.sendall(str(risultato).encode("UTF-8"))
                
            except json.JSONDecodeError:
                print(f"Errore: Ricevuto JSON malformato da {addr_client}")
    except Exception as e:
        print(f"Errore nel thread {addr_client}: {e}")
    finally:
        print(f"--- Connessione chiusa con {addr_client} ---")
        sock_service.close()

def avvia_server(indirizzo, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_listen:
        sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_listen.bind((indirizzo, porta))
        sock_listen.listen(5)
        print(f" ---- Server in ascolto su {indirizzo}:{porta} ---- ")
        
        while True:
            sock_service, address_client = sock_listen.accept()
            Thread(target=ricevi_comandi, args=(sock_service, address_client), daemon=True).start()

IP = "127.0.0.1"
PORTA = 65432
DIM_BUFFER = 1024

avvia_server(IP, PORTA)