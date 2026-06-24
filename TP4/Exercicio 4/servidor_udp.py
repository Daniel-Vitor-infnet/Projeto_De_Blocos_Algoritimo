import socket

HOST = '127.0.0.1'
PORT = 65433 # Usando uma porta diferente do TCP para não dar conflito

# SOCK_DGRAM = UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"[UDP] Servidor aguardando datagramas em {HOST}:{PORT}...")
    
    while True:
        # UDP não tem accept() nem listen(), ele só recebe de quem mandar
        data, addr = s.recvfrom(1024)
        print(f"[UDP] Mensagem recebida de {addr}: {data.decode('utf-8')}")
        
        # Manda resposta direto pro endereço (addr) que enviou
        s.sendto(b"Recebido pelo Servidor UDP, cambio!", addr)