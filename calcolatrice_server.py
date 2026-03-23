import socket, json

SERVER_IP="127.0.0.1"
SERVER_PORT=5005
BUFFER_SIZE=1024

#Creazione del socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((SERVER_IP, SERVER_PORT))

while True:
    data, addr = s.recvfrom(1024)
    if not data:
        break
    data=data.decode()

    data=json.loads(data)
    primoNumero=data["primoNumero"]
    operazione=data["operazione"]
    secondoNumero=["secondoNumero"]

    reply=""
    if operazione=="+":
        reply=str(primoNumero+secondoNumero)
    elif operazione=="-":
        reply=str(primoNumero-secondoNumero)
    elif operazione=="*":
        reply=str(primoNumero*secondoNumero)
    elif operazione=="/":
        if secondoNumero!=0:
            reply=str(primoNumero/secondoNumero)
        else:
            reply="Errore: divisione per zero"

    s.sendto(reply.encode("UTF-8"), addr)
