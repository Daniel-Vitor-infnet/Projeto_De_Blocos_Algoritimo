import socket

# Configurações do Servidor B
HOST = '127.0.0.1'
PORT = 65432        # Porta de comunicação

# AF_INET = IPv4 | SOCK_STREAM = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen() # Fica escutando conexões
    print(f"[TCP] Servidor aguardando conexões em {HOST}:{PORT}...")
    
    conn, addr = s.accept() # Aceita a conexão do Cliente A
    with conn:
        print(f"[TCP] Conectado a: {addr}")
        while True:
            data = conn.recv(1024) # Recebe até 1024 bytes
            if not data:
                break
            print(f"[TCP] Mensagem do Cliente: {data.decode('utf-8')}")
            # Manda resposta de volta
            conn.sendall(b"Recebido pelo Servidor TCP, cambio!")