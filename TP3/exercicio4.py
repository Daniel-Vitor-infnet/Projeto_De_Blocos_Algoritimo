import ipaddress

class TrieNode:
    def __init__(self, path=""):
        self.path = path 
        self.route_id = None
        self.left = None  # Ramo para '0'
        self.right = None # Ramo para '1'

class BuscadorLPM:
    def __init__(self):
        self.raiz = TrieNode()

    def _ip_para_binario(self, ip_str):
        """Converte qualquer IP (v4 ou v6) para uma string de bits '0101...'"""
        ip = ipaddress.ip_address(ip_str)
        return ''.join(f'{b:08b}' for b in ip.packed)

    def insert(self, prefixo: str, route_id: int):
        ip_str, tamanho_prefixo = prefixo.split('/')
        tamanho_prefixo = int(tamanho_prefixo)
        
        # Pega apenas a porção de bits que importa para a máscara
        bits = self._ip_para_binario(ip_str)[:tamanho_prefixo]
        
        atual = self.raiz
        i = 0
        
        while i < len(bits):
            char_atual = bits[i]
            filho = atual.left if char_atual == '0' else atual.right
            
            # Caso 1: Não tem caminho para esse lado, cria um nó folha direto com os bits restantes
            if not filho:
                novo_no = TrieNode(bits[i:])
                novo_no.route_id = route_id
                if char_atual == '0':
                    atual.left = novo_no
                else:
                    atual.right = novo_no
                return

            # Caso 2: Tem um filho. Vamos ver quantos bits o caminho atual compartilha com o nó existente
            resto_bits = bits[i:]
            lcp_len = 0 
            while (lcp_len < len(filho.path) and 
                   lcp_len < len(resto_bits) and 
                   filho.path[lcp_len] == resto_bits[lcp_len]):
                lcp_len += 1
            
            if lcp_len == len(filho.path):
                # O caminho do filho bateu totalmente ai terá o avanço para ele
                atual = filho
                i += lcp_len
            else:
                # Caso 3: Divergência (split)
                no_quebrado = TrieNode(filho.path[:lcp_len])
                
                # O nó antigo desce um nível
                filho.path = filho.path[lcp_len:]
                if filho.path[0] == '0':
                    no_quebrado.left = filho
                else:
                    no_quebrado.right = filho
                
                # O novo nó quebrado assume o lugar
                if char_atual == '0':
                    atual.left = no_quebrado
                else:
                    atual.right = no_quebrado
                
                # Cria a nova bifurcação para os bits inseridos (se sobrou algo)
                if lcp_len == len(resto_bits):
                    no_quebrado.route_id = route_id
                else:
                    nova_folha = TrieNode(resto_bits[lcp_len:])
                    nova_folha.route_id = route_id
                    if resto_bits[lcp_len] == '0':
                        no_quebrado.left = nova_folha
                    else:
                        no_quebrado.right = nova_folha
                return
                
        # Se chegou aqui, os bits bateram examente com um nó já existente (ex: Rota Default 0.0.0.0/0)
        atual.route_id = route_id

    def lookup(self, ip: str) -> int:
        bits = self._ip_para_binario(ip)
        atual = self.raiz
        ultimo_match = atual.route_id # Salva a rota default, se existir
        
        i = 0
        while i < len(bits):
            char_atual = bits[i]
            filho = atual.left if char_atual == '0' else atual.right
            
            if not filho:
                break
                
            resto_bits = bits[i:]
            
            # Se a string IP começa com o caminho completo do nó filho
            if resto_bits.startswith(filho.path):
                if filho.route_id is not None:
                    ultimo_match = filho.route_id # Atualiza o LPM
                atual = filho
                i += len(filho.path)
            else:
                # Divergiu antes de completar o nó, interrompe a busca
                break
                
        return ultimo_match


# TESTES ---
if __name__ == "__main__":
    tabela_roteamento = [
        ("192.168.0.0/16", 10),
        ("192.168.1.0/24", 20),
        ("192.168.1.128/25", 30),
        ("10.0.0.0/8", 40),
        ("0.0.0.0/0", 50),
        ("2001:db8::/32", 100),
        ("2001:db8:a::/48", 200)
    ]

    roteador = BuscadorLPM()
    
    print("Carregando Tabela de Roteamento...")
    for cidr, id_rota in tabela_roteamento:
        roteador.insert(cidr, id_rota)

    buscas = [
        ("192.168.0.50", 10),
        ("192.168.1.20", 20),
        ("192.168.1.150", 30),
        ("10.255.0.1", 40),
        ("8.8.8.8", 50),
        ("2001:db8:cafe::1", 100),
        ("2001:db8:a:b::1", 200)
    ]

    print("\n--- CASOS DE TESTE ---")
    for ip_alvo, id_esperado in buscas:
        id_retornado = roteador.lookup(ip_alvo)
        status = "Aprovado" if id_retornado == id_esperado else "Falhou"
        print(f"IP: {ip_alvo.ljust(18)} | Retornou: {str(id_retornado).ljust(4)} | Esperado: {id_esperado} {status}")