import sys
import socket
import threading

# HEX_FILTER pour afficher les données de façon lisible
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

# Fonction pour afficher les données en hexadécimal
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode(errors="replace")

    results = []
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length * 3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')

    if show:
        for line in results:
            print(line)
    else:
        return results

# Fonction pour recevoir des données d'une connexion
def receive_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer

# Fonction pour modifier une requête avant de l'envoyer (peut être personnalisé)
def request_handler(buffer):
    return buffer

# Fonction pour modifier une réponse avant de l'envoyer (peut être personnalisé)
def response_handler(buffer):
    return buffer

# Fonction qui gère le proxy entre client et serveur distant
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Reçu %d octets du serveur distant." % len(remote_buffer))
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print("[==>] Reçu %d octets du client local." % len(local_buffer))
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Envoyé au serveur distant.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Reçu %d octets du serveur distant." % len(remote_buffer))
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Envoyé au client local.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] Plus de données, fermeture des connexions.")
            break

# Fonction qui lance le serveur proxy
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print(f"[!!] Erreur de liaison : {e}")
        sys.exit(0)

    print(f"[*] Écoute sur {local_host}:{local_port}")
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        print(f"[==>] Connexion entrante de {addr[0]}:{addr[1]}")

        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

# Fonction principale pour lire les arguments et démarrer le proxy
def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Exemple: ./proxy.py 127.0.0.1 9000 example.com 80 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5].lower() == "true"

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == "__main__":
    main()
