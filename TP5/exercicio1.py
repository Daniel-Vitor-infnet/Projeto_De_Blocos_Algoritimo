# --- DADOS DE ENTRADA ---
NUM_CIDADES = 30
CONEXOES = [
    (0, 1, 45, 3), (0, 2, 60, 8), (0, 3, 75, 12), (1, 2, 20, 2), (1, 4, 55, 6),
    (2, 3, 35, 4), (2, 5, 40, 5), (3, 6, 80, 10), (4, 5, 15, 1), (4, 7, 90, 14),
    (5, 6, 30, 3), (5, 8, 50, 7), (6, 9, 65, 9), (7, 8, 25, 2), (7, 10, 70, 11),
    (8, 9, 45, 5), (8, 11, 60, 8), (9, 12, 85, 13), (10, 11, 15, 1), (10, 13, 50, 6),
    (11, 12, 40, 4), (11, 14, 55, 7), (12, 15, 75, 10), (13, 14, 30, 3), (13, 16, 65, 9),
    (14, 15, 35, 4), (14, 17, 45, 6), (15, 18, 90, 15), (16, 17, 20, 2), (16, 19, 55, 8),
    (17, 18, 40, 5), (17, 20, 60, 9), (18, 21, 80, 12), (19, 20, 25, 3), (19, 22, 70, 11),
    (20, 21, 35, 4), (20, 23, 50, 7), (21, 24, 75, 10), (22, 23, 15, 1), (22, 25, 60, 8),
    (23, 24, 45, 6), (23, 26, 55, 7), (24, 27, 90, 14), (25, 26, 30, 3), (25, 28, 65, 9),
    (26, 27, 40, 5), (26, 29, 70, 11), (27, 29, 50, 6), (28, 29, 25, 2), (0, 4, 110, 18),
    (1, 5, 85, 11), (2, 6, 95, 14), (3, 9, 120, 22), (4, 8, 70, 9), (5, 9, 60, 8),
    (6, 12, 110, 16), (7, 11, 65, 9), (8, 12, 80, 11), (9, 15, 130, 24), (10, 14, 55, 7),
    (11, 15, 70, 9), (12, 18, 115, 19), (13, 17, 60, 8), (14, 18, 75, 10), (15, 21, 140, 25),
    (16, 20, 65, 9), (17, 21, 85, 12), (18, 24, 125, 20), (19, 23, 60, 8), (20, 24, 80, 11),
    (21, 27, 135, 23), (22, 26, 55, 7), (23, 27, 75, 10), (24, 29, 110, 17), (0, 7, 200, 35),
    (3, 12, 180, 28), (10, 19, 150, 22), (13, 22, 140, 21), (16, 25, 160, 26), (1, 8, 95, 13),
    (2, 9, 105, 15), (7, 13, 85, 12), (11, 17, 90, 13), (19, 25, 80, 12), (20, 26, 85, 13)
]

# --- ETAPA 1: KRUSKAL (Menor Custo para Infraestrutura) ---
def resolver_etapa_infraestrutura():
    # Estrutura Union-Find (para detectar ciclos)
    pai = list(range(NUM_CIDADES))
    
    def encontrar(i):
        if pai[i] == i:
            return i
        pai[i] = encontrar(pai[i]) # Compressão de caminho
        return pai[i]
        
    def unir(i, j):
        raiz_i = encontrar(i)
        raiz_j = encontrar(j)
        if raiz_i != raiz_j:
            pai[raiz_i] = raiz_j
            return True
        return False

    # Ordena as conexões pelo custo (índice 2 da tupla)
    conexoes_ordenadas = sorted(CONEXOES, key=lambda x: x[2])
    
    rede_escolhida = []
    custo_total = 0
    
    for origem, destino, custo, latencia in conexoes_ordenadas:
        # Se unir não formar ciclo, adicionamos à rede
        if unir(origem, destino):
            rede_escolhida.append((origem, destino, custo))
            custo_total += custo

    print("="*50)
    print(" ETAPA 1: REDE DE INFRAESTRUTURA (MENOR CUSTO)")
    print("="*50)
    print("Conexões escolhidas (Origem -> Destino | Custo):")
    for orig, dest, c in rede_escolhida:
        print(f"Cidade {orig:02d} <-> Cidade {dest:02d} | Custo: {c}")
    print(f"\n>> CUSTO TOTAL DA INFRAESTRUTURA: {custo_total}\n")


# --- ETAPA 2: DIJKSTRA (Pior Latência de Comunicação / Menor Caminho) ---
def resolver_etapa_operacao():
    """
     Montando a Lista de Adjacência usando todas as conexões
     Grafo não direcionado: Cidade A vai pra B e B vai pra A
    """
    grafo = {i: [] for i in range(NUM_CIDADES)}
    for origem, destino, custo, latencia in CONEXOES:
        grafo[origem].append((destino, latencia))
        grafo[destino].append((origem, latencia))

    # Inicializa distâncias com infinito e Cidade 0 com 0
    latencias_acumuladas = {i: float('inf') for i in range(NUM_CIDADES)}
    latencias_acumuladas[0] = 0
    
    nao_visitados = set(range(NUM_CIDADES))

    # Loop principal do Dijkstra Manual
    while nao_visitados:
        # Pega a cidade não visitada com a menor latência acumulada até agora
        cidade_atual = min(nao_visitados, key=lambda cidade: latencias_acumuladas[cidade])
        
        nao_visitados.remove(cidade_atual)
        
        # Se a menor latência for infinito, nós restantes estão isolados
        if latencias_acumuladas[cidade_atual] == float('inf'):
            break

        # Analisa os vizinhos da cidade atual
        for vizinho, latencia_trecho in grafo[cidade_atual]:
            if vizinho in nao_visitados:
                nova_latencia = latencias_acumuladas[cidade_atual] + latencia_trecho
                # Se encontrou um caminho mais rápido, atualiza
                if nova_latencia < latencias_acumuladas[vizinho]:
                    latencias_acumuladas[vizinho] = nova_latencia

    print("="*50)
    print(" ETAPA 2: OPERAÇÃO (LATÊNCIA ACUMULADA DA CIDADE 0)")
    print("="*50)
    print("Latência da Cidade 0 para todas as outras (em ms):")
    
    pior_latencia = 0
    cidade_pior_latencia = -1
    
    for cidade in range(1, NUM_CIDADES):
        lat = latencias_acumuladas[cidade]
        print(f"Da Cidade 0 para a Cidade {cidade:02d} -> {lat} ms")
        if lat > pior_latencia:
            pior_latencia = lat
            cidade_pior_latencia = cidade
            
    print(f"\n>> PIOR LATÊNCIA DA REDE: {pior_latencia} ms (Destino: Cidade {cidade_pior_latencia})")


# Executa o programa
if __name__ == "__main__":
    resolver_etapa_infraestrutura()
    resolver_etapa_operacao()