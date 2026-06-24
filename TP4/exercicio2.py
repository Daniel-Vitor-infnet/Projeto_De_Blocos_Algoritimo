class NoTrie:
    def __init__(self):
        self.filhos = {}
        self.fim_palavra = False

class Trie:
    def __init__(self):
        self.raiz = NoTrie()

    # 1. Inserir palavras
    def inserir(self, palavra):
        atual = self.raiz
        for letra in palavra:
            if letra not in atual.filhos:
                atual.filhos[letra] = NoTrie()
            atual = atual.filhos[letra]
        atual.fim_palavra = True

    # 2. Busca
    def buscar(self, palavra):
        atual = self.raiz
        for letra in palavra:
            if letra not in atual.filhos:
                return False
            atual = atual.filhos[letra]
        return atual.fim_palavra

    # 3. Remover
    def remover(self, palavra):
        def _remover(no, palavra, profundidade):
            if profundidade == len(palavra):
                if not no.fim_palavra: return False
                no.fim_palavra = False
                return len(no.filhos) == 0

            letra = palavra[profundidade]
            if letra not in no.filhos:
                return False

            pode_apagar = _remover(no.filhos[letra], palavra, profundidade + 1)

            if pode_apagar:
                del no.filhos[letra]
                return len(no.filhos) == 0 and not no.fim_palavra
            return False

        _remover(self.raiz, palavra, 0)

    # 4. Listar todas
    def listar_todas(self):
        resultado = []
        def _dfs(no, caminho):
            if no.fim_palavra:
                resultado.append("".join(caminho))
            for letra, filho in no.filhos.items():
                caminho.append(letra)
                _dfs(filho, caminho)
                caminho.pop()
        _dfs(self.raiz, [])
        return resultado

    # 5. Autocompletar
    def autocompletar(self, prefixo):
        atual = self.raiz
        for letra in prefixo:
            if letra not in atual.filhos:
                return []
            atual = atual.filhos[letra]

        resultado = []
        def _dfs(no, caminho):
            if no.fim_palavra:
                resultado.append(prefixo + "".join(caminho))
            for letra, filho in no.filhos.items():
                caminho.append(letra)
                _dfs(filho, caminho)
                caminho.pop()
                
        _dfs(atual, [])
        return resultado

    # 6. Autocorreção (Levenshtein)
    def autocorrigir(self, palavra):
        if self.buscar(palavra):
            return palavra
            
        def distancia(s1, s2):
            if len(s1) < len(s2): return distancia(s2, s1)
            if len(s2) == 0: return len(s1)
            anterior = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                atual = [i + 1]
                for j, c2 in enumerate(s2):
                    insercoes = anterior[j + 1] + 1
                    delecoes = atual[j] + 1
                    substituicoes = anterior[j] + (c1 != c2)
                    atual.append(min(insercoes, delecoes, substituicoes))
                anterior = atual
            return anterior[-1]

        palavras = self.listar_todas()
        if not palavras: return None
        
        return min(palavras, key=lambda p: distancia(palavra, p))


# --- 7. TESTES ---
if __name__ == "__main__":
    trie = Trie()
    
    # As 100 mais comuns
    top_100_ptbr = [
        "que", "não", "o", "de", "a", "e", "é", "do", "da", "um", "com", "para", "se", "uma", 
        "os", "na", "no", "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele", 
        "das", "tem", "à", "seu", "sua", "ou", "ser", "quando", "muito", "há", "nos", "já", 
        "está", "eu", "também", "só", "pelo", "pela", "até", "isso", "ela", "entre", "era", 
        "depois", "sem", "mesmo", "aos", "ter", "seus", "quem", "nas", "me", "esse", "eles", 
        "estão", "você", "tinha", "foram", "essa", "num", "nem", "suas", "meu", "às", "minha", 
        "têm", "numa", "pelos", "elas", "havia", "seja", "qual", "será", "nós", "tenho", "lhe", 
        "deles", "essas", "esses", "pode", "este", "fazer", "sobre", "vez", "mesma", "tudo", 
        "outros", "ano", "dois", "vezes", "onde", "agora", "cada", "ainda"
    ]

    print("--- RODANDO TESTES ---")

    # 1
    for p in top_100_ptbr: trie.inserir(p)
    print("1. Inserção: OK (100 palavras)")

    # 2
    print(f"2. Busca por 'quando': {trie.buscar('quando')} | Busca por 'python': {trie.buscar('python')}")

    # 3
    print(f"3. Autocompletar 'es': {trie.autocompletar('es')}")

    # 4
    print(f"4. Autocorreção 'quendo' -> {trie.autocorrigir('quendo')}")
    print(f"   Autocorreção 'vose' -> {trie.autocorrigir('vose')}")

    # 5
    trie.remover("você")
    print(f"5. Remoção de 'você'. Existe agora? {trie.buscar('você')}")

    # 6
    todas = trie.listar_todas()
    print(f"6. Total na árvore: {len(todas)}. Exemplo: {todas[:5]}")