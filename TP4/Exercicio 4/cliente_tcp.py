import socket

HOST = '127.0.0.1'  # IP do Servidor B
PORT = 65432        # Mesma porta do servidor

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # Exclusivo do TCP: estabelece a conexão primeiro
    print(f"[TCP] Conectado ao servidor {HOST}:{PORT}")
    
    mensagem = "Salve, Servidor TCP! Aqui eh o Cliente A."
    s.sendall(mensagem.encode('utf-8'))
    
    data = s.recv(1024)
    print(f"[TCP] Resposta do Servidor: {data.decode('utf-8')}")