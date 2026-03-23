import json
import socket

SERVER_IP="127.0.0.1"
SERVER_PORT=5005
BUFFER_SIZE=1024
NUM_MESSAGES=5

#Creazione del socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(NUM_MESSAGES):
    primoNumero=float(input("Inserisci il primo numero: "))
    operazione = input("Inserisci l'operazione (simbolo)")
    secondoNumero=float(input("Inserisci il secondo numero: "))
    messaggio={
        "primoNumero":primoNumero,
        "operazione":operazione,
        "SecondoNumero": secondoNumero,
    }
    messaggio=json.dumps(messaggio)

    s.sendto(messaggio.encode("UTF-8"), (SERVER_IP, SERVER_PORT))
    data, addr = s.recvfrom(BUFFER_SIZE)
    print("Risultato: ", data.decode())

s.close()