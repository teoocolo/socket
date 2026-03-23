import socket
import json

SERVER_IP="127.0.0.1"
SERVER_PORT=65432
BUFFER_SIZE=1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_client:
    sock_client.connect((SERVER_IP, SERVER_PORT))
    print(f"Connesso al server {SERVER_IP}:{SERVER_PORT}")
    while True:
        primoNumero=float(input("Inserisci il primo numero: "))
        operazione = input("Inserisci l'operazione (simbolo): ")
        secondoNumero=float(input("Inserisci il secondo numero: "))
        messaggio={
            "primoNumero": primoNumero,
            "operazione": operazione,
            "secondoNumero": secondoNumero
        }
        messaggio = json.dumps(messaggio)
        sock_client.sendall(messaggio.encode())
        data = sock_client.recv(BUFFER_SIZE).decode()
        print(f"Risultato: {data}")
