import socket
import ssl

HOST = '127.0.0.1'
PORT = 8443

# Configura o cliente 
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE 

with socket.create_connection((HOST, PORT)) as sock:
    # Tunelando a conexão
    with context.wrap_socket(sock, server_hostname=HOST) as ssock:
        print(f"[Cliente] Conectado via TLS a {HOST}:{PORT}")
        
        # A mensagem super secreta
        mensagem = "AUTH_TOKEN:XYZ123:CMD:REBOOT_SERVER"
        ssock.sendall(mensagem.encode('utf-8'))
        print(f"[Cliente] Mensagem original enviada: {mensagem}")