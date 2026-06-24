import pcapy
import string

# Encontra a interface de rede local (Loopback/Localhost)
devices = pcapy.findalldevs()
lo_device = None
for d in devices:
    if "Loopback" in d or d == "lo" or d == "lo0":
        lo_device = d
        break
if not lo_device:
    lo_device = devices[0] # Tenta pegar a primeira se não achar pelo nome

print(f"[*] Iniciando captura na interface {lo_device} (Porta 8443)...")

# Abre a placa de rede
cap = pcapy.open_live(lo_device, 65536, 1, 0)

# Filtro BPF para pegar só a porta do nosso servidor
cap.setfilter("tcp port 8443")

def analisar_pacote(header, data):
    tamanho = len(data)
    # Ignora pacotinhos pequenos que são só confirmação de conexão (ACKs)
    if tamanho > 60: 
        print(f"\n[+] Pacote TCP Capturado! Tamanho: {tamanho} bytes.")
        
        # Decodifica tentando extrair só caracteres que o ser humano consegue ler
        caracteres_imprimiveis = set(string.printable)
        texto_convertido = ''.join(filter(lambda x: x in caracteres_imprimiveis, data.decode('latin-1', errors='ignore')))
        
        print(f"[Dados Brutos do Payload]: {repr(data[:30])}...")
        # Mostra o texto legível. Se a criptografia funcionar, isso será um lixo ilegível
        print(f"[Texto Convertido]: {texto_convertido[20:80]}...") 
        
        # A prova real
        if 'AUTH_TOKEN' in texto_convertido:
            print("[-] ALERTA CRÍTICO: Padrão 'AUTH_TOKEN' ENCONTRADO! (Vazamento de dados)")
        else:
            print("[-] Alerta: Padrão 'AUTH_TOKEN' NÃO encontrado. Os dados estão devidamente cifrados via TLS.")

# Fica escutando pacotes infinitamente
cap.loop(-1, analisar_pacote)