# Client TCP multithread che invia NUM_WORKERS richieste contemporanee al server
# Ogni richiesta contiene un'operazione aritmetica da eseguire

import socket         # Per la comunicazione di rete
import json           # Per la codifica/decodifica JSON
import random         # Per generare numeri casuali
import time           # Per misurare i tempi di esecuzione
import threading      # Per gestire l'esecuzione parallela (multithreading)

# --- Configurazione ---
HOST = "127.0.0.1"           # IP del server
PORT = 65432                # Porta del server (assicurarsi che il server stia ascoltando su questa)
NUM_WORKERS = 15            # Numero di richieste (thread) da inviare in parallelo
OPERAZIONI = ["+", "-", "*", "/", "%"]  # Lista delle operazioni consentite

# Funzione che genera e invia richieste al server
def genera_richieste(address, port):
    # Creazione del socket TCP per comunicare con il server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
        sock_service.connect((address, port))  # Connessione al server

        # Gemera numeri e operazione a caso per la richiesta
        primoNumero = random.randint(0, 100)
        operazione = OPERAZIONI[random.randint(0, 3)]  # Scegli operazione a caso (tra le prime 4)
        secondoNumero = random.randint(0, 100)

        # Crea un messaggio con i dati della richiesta e lo codifica in JSON
        messaggio = {
            "primoNumero": primoNumero,
            "operazione": operazione,
            "secondoNumero": secondoNumero
        }
        messaggio = json.dumps(messaggio)

        # Invia il messaggio al server (codificato in UTF-8)
        sock_service.sendall(messaggio.encode("UTF-8"))

        # Misura il tempo di attesa per la risposta del server
        start_time_thread = time.time()

        # Attende la risposta del server (fino a 1024 byte) e la decodifica
        data = sock_service.recv(1024)

    # Calcola il tempo di esecuzione per questa richiesta e stampa la risposta ricevuta
    end_time_thread = time.time()
    print("Received: ", data.decode())
    print(f"{threading.current_thread().name} exec time = ", end_time_thread - start_time_thread)

# --- Punto di ingresso del programma ---
if __name__ == "__main__":
    start_time = time.time()  # Tempo di inizio totale

    # Crea una lista di thread, ognuno dei quali esegue la funzione genera_richieste
    threads = [
        threading.Thread(target=genera_richieste, args=(HOST, PORT))
        for _ in range(NUM_WORKERS)
    ]

    # Avvia tutti i thread per eseguire le richieste in parallelo
    [thread.start() for thread in threads]

    # Attende che tutti i thread abbiano completato l'esecuzione prima di procedere
    [thread.join() for thread in threads]

    end_time = time.time()  # Tempo di fine totale

    # Stampa il tempo complessivo impiegato per eseguire tutte le richieste
    print("Tempo totale impiegato = ", end_time - start_time)