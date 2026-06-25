class No:
    def __init__(self, chave, signi):
        self.chave = chave
        self.signi = signi
        self.esq = None
        self.dir = None
        self.altura = 1  # Altura para calcular o balanceamento da árvore

class Dicionario:
    def __init__(self):
        self.raiz = None
        self.tamanho = 0 
        
    # --- funções auxiliares ---
    def _get_altura(self, no):
        if not no:
            return 0
        return no.altura

    def _get_balanceamento(self, no):
        if not no:
            return 0
        return self._get_altura(no.esq) - self._get_altura(no.dir)

    def _rotacao_direita(self, y):
        x = y.esq
        T2 = x.dir
        # faz a rotação
        x.dir = y
        y.esq = T2
        # Atualiza alturas
        y.altura = 1 + max(self._get_altura(y.esq), self._get_altura(y.dir))
        x.altura = 1 + max(self._get_altura(x.esq), self._get_altura(x.dir))
        return x

    def _rotacao_esquerda(self, x):
        y = x.dir
        T2 = y.esq
        # Faz a rotação
        y.esq = x
        x.dir = T2
        # Atualiza alturas
        x.altura = 1 + max(self._get_altura(x.esq), self._get_altura(x.dir))
        y.altura = 1 + max(self._get_altura(y.esq), self._get_altura(y.dir))
        return y

    # a. Inserir verbetes e seus significados 
    def inserir(self, chave, signi):
        # A busca rápida evita somar no tamanho se a palavra já existe
        if self.buscar(chave) == "Palavra não encontrada.":
            self.tamanho += 1
        self.raiz = self._inserir_recursivo(self.raiz, chave, signi)
            
    def _inserir_recursivo(self, no_atual, chave, signi):
        # Inserção normal de BST
        if not no_atual:
            return No(chave, signi)
        
        if chave < no_atual.chave:
            no_atual.esq = self._inserir_recursivo(no_atual.esq, chave, signi)
        elif chave > no_atual.chave:
            no_atual.dir = self._inserir_recursivo(no_atual.dir, chave, signi)
        else:
            no_atual.signi = signi # Atualiza se já existir
            return no_atual

        # Atualiza a altura do nó pai
        no_atual.altura = 1 + max(self._get_altura(no_atual.esq), self._get_altura(no_atual.dir))
        # Verifica o fator de balanceamento
        balanco = self._get_balanceamento(no_atual)

        # Casos de Rotação
        # Caso Esquerda-Esquerda (LL)
        if balanco > 1 and chave < no_atual.esq.chave:
            return self._rotacao_direita(no_atual)
        # Caso Direita-Direita (RR)
        if balanco < -1 and chave > no_atual.dir.chave:
            return self._rotacao_esquerda(no_atual)
        # Caso Esquerda-Direita (LR)
        if balanco > 1 and chave > no_atual.esq.chave:
            no_atual.esq = self._rotacao_esquerda(no_atual.esq)
            return self._rotacao_direita(no_atual)
        # Caso Direita-Esquerda (RL)
        if balanco < -1 and chave < no_atual.dir.chave:
            no_atual.dir = self._rotacao_direita(no_atual.dir)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    # Buscar verbetes
    def buscar(self, chave):
        no = self._buscar_recursivo(self.raiz, chave)
        if no:
            return f"{no.chave}: {no.signi}"
        return "Palavra não encontrada."
    
    def _buscar_recursivo(self, no_atual, chave):
        if no_atual is None:
            return None
        if chave == no_atual.chave:
            return no_atual
        elif chave < no_atual.chave:
            return self._buscar_recursivo(no_atual.esq, chave)
        else:
            return self._buscar_recursivo(no_atual.dir, chave)

    # Listar palavras contidas no dicionário
    def listar(self):
        print("Palavras no Dicionário:")
        self._listar_recursivo(self.raiz) 
        
    def _listar_recursivo(self, no_atual):
        if no_atual is not None:
            self._listar_recursivo(no_atual.esq)
            print(f"- {no_atual.chave}: {no_atual.signi}")
            self._listar_recursivo(no_atual.dir)

    # Remover verbetes
    def remover(self, chave):
        if self.buscar(chave) != "Palavra não encontrada.":
            self.raiz = self._remover_recursivo(self.raiz, chave)
            self.tamanho -= 1
            
    def _remover_recursivo(self, no_atual, chave):
        # Remoção de BST
        if not no_atual:
            return no_atual

        if chave < no_atual.chave:
            no_atual.esq = self._remover_recursivo(no_atual.esq, chave)
        elif chave > no_atual.chave:
            no_atual.dir = self._remover_recursivo(no_atual.dir, chave)
        else:
            if no_atual.esq is None:
                return no_atual.dir
            elif no_atual.dir is None:
                return no_atual.esq
            
            temp = self._minimo(no_atual.dir)
            no_atual.chave, no_atual.signi = temp.chave, temp.signi
            no_atual.dir = self._remover_recursivo(no_atual.dir, temp.chave)

        if not no_atual:
            return no_atual

        # Atualiza a altura
        no_atual.altura = 1 + max(self._get_altura(no_atual.esq), self._get_altura(no_atual.dir))

        # Verifica o fator de balanceamento
        balanco = self._get_balanceamento(no_atual)

        # Casos de Rotação
        # Caso LL
        if balanco > 1 and self._get_balanceamento(no_atual.esq) >= 0:
            return self._rotacao_direita(no_atual)
        # Caso LR
        if balanco > 1 and self._get_balanceamento(no_atual.esq) < 0:
            no_atual.esq = self._rotacao_esquerda(no_atual.esq)
            return self._rotacao_direita(no_atual)
        # Caso RR
        if balanco < -1 and self._get_balanceamento(no_atual.dir) <= 0:
            return self._rotacao_esquerda(no_atual)
        # Caso RL
        if balanco < -1 and self._get_balanceamento(no_atual.dir) > 0:
            no_atual.dir = self._rotacao_direita(no_atual.dir)
            return self._rotacao_esquerda(no_atual)

        return no_atual
    
    def _minimo(self, no_atual):
        while no_atual.esq is not None: 
            no_atual = no_atual.esq
        return no_atual

    # Altura da árvore
    def altura(self):
        if self.raiz is None:
            return 0
        return self.raiz.altura

    # Número de itens armazenados
    def numero_itens(self):
        return self.tamanho


# TESTE
dicionario = Dicionario()
# Inserindo de forma que forçaria a árvore a ficar desbalanceada
dicionario.inserir("Algoritmo", "Passos para resolver um problema complexo")
dicionario.inserir("Erro", "Erro no código")
dicionario.inserir("Python", "Linguagem de programação de baixo nível")
dicionario.inserir("Variavel", "Espaço na memória")
dicionario.inserir("Zero", "Número nulo")

# TESTE Métodos
dicionario.listar()
print("-" * 30)
print(f"Busca por 'Python': {dicionario.buscar('Python')}")
print(f"Altura: {dicionario.altura()}")
print(f"Itens: {dicionario.numero_itens()}")
print("-" * 30)
print("Removendo 'Erro'...")
dicionario.remover("Erro")
dicionario.listar()
print(f"Nova Altura: {dicionario.altura()}")
print(f"Novos Itens: {dicionario.numero_itens()}")