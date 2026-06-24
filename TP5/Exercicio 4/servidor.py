import socket
import ssl

HOST = '127.0.0.1'
PORT = 8443

# Configura o contexto SSL/TLS carregando os certificados que criamos
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"[Servidor] Aguardando conexões TLS seguras em {HOST}:{PORT}...")
    
    # O "wrap_socket" transforma o socket comum num túnel criptografado
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, addr = ssock.accept()
        with conn:
            print(f"[Servidor] Conexão segura estabelecida com {addr}")
            data = conn.recv(1024)
            print(f"[Servidor] Comando Seguro Recebido: {data.decode('utf-8')}")