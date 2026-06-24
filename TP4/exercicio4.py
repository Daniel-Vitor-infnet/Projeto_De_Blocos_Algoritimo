from collections import defaultdict, deque

class GrafoLabirinto:
    def __init__(self):
        # A. Representação computacional: Grafo usando Lista de Adjacência.
        # Os vértices são as encruzilhadas/portas e as arestas são os corredores.
        self.grafo = defaultdict(list)

    def adicionar_corredor(self, u, v):
        self.grafo[u].append(v)
        self.grafo[v].append(u)

    # B. DFS (Busca em Profundidade) usando Pilha
    def resolver_dfs(self, inicio, saida):
        # Pilha armazena tuplas: (nó_atual, caminho_ate_agora)
        pilha = [(inicio, [inicio])]
        visitados = set()

        while pilha:
            vertice, caminho = pilha.pop() # LIFO (Último a entrar, primeiro a sair)

            if vertice == saida:
                return caminho

            if vertice not in visitados:
                visitados.add(vertice)
                # Adiciona os vizinhos na pilha
                for vizinho in self.grafo[vertice]:
                    if vizinho not in visitados:
                        pilha.append((vizinho, caminho + [vizinho]))
        
        return None # Sem saída

    # C. BFS (Busca em Largura) usando Fila
    def resolver_bfs(self, inicio, saida):
        # Fila armazena tuplas: (nó_atual, caminho_ate_agora)
        fila = deque([(inicio, [inicio])])
        visitados = set()

        while fila:
            vertice, caminho = fila.popleft() # FIFO (Primeiro a entrar, primeiro a sair)

            if vertice == saida:
                return caminho

            if vertice not in visitados:
                visitados.add(vertice)
                # Adiciona os vizinhos na fila
                for vizinho in self.grafo[vertice]:
                    if vizinho not in visitados:
                        fila.append((vizinho, caminho + [vizinho]))
        
        return None # Sem saída

# --- TESTES ---
if __name__ == "__main__":
    labirinto = GrafoLabirinto()

    # A bifurca em B e C. C é um beco sem saída. B vai para D. D bifurca para E (beco) e F (Saída).
    arestas = [
        ('A', 'B'), ('A', 'C'), 
        ('B', 'D'), 
        ('D', 'E'), ('D', 'F'),
        ('F', 'G') # F é a saída, mas tem um corredor extra depois só de zoas
    ]

    for u, v in arestas:
        labirinto.adicionar_corredor(u, v)

    entrada = 'A'
    saida = 'F'

    print("--- RESULTADOS DA BUSCA NO LABIRINTO ---")
    
    caminho_dfs = labirinto.resolver_dfs(entrada, saida)
    print(f"Caminho encontrado via DFS (Pilha): {' -> '.join(caminho_dfs)}")

    caminho_bfs = labirinto.resolver_bfs(entrada, saida)
    print(f"Caminho encontrado via BFS (Fila):  {' -> '.join(caminho_bfs)}")