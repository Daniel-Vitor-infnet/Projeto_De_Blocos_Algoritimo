class No:
    def __init__(self, chave, signi):
        self.chave = chave
        self.signi = signi
        self.esq = None
        self.dir = None
        
class Dicionario:
    def __init__(self):
        self.raiz = None
        self.tamanho = 0 
        
    # Inserir verbetes e seus significados 
    def inserir(self, chave, signi):
        if self.raiz is None:
            self.raiz = No(chave, signi)
            self.tamanho += 1
        else:
            self._inserir_recursivo(self.raiz, chave, signi)
            
    def _inserir_recursivo(self, no_atual, chave, signi):
        if chave < no_atual.chave:
            if no_atual.esq is None:
                no_atual.esq = No(chave, signi)
                self.tamanho += 1
            else:
                self._inserir_recursivo(no_atual.esq, chave, signi)
        elif chave > no_atual.chave:
            if no_atual.dir is None:
                no_atual.dir = No(chave, signi)
                self.tamanho += 1
            else:
                self._inserir_recursivo(no_atual.dir, chave, signi)
        else:
            no_atual.signi = signi # Caso a palavra exista ela sera atualizada

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

    # c. Listar palavras contidas no dicionário
    def listar(self):
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
        if no_atual is None:
            return no_atual
        if chave < no_atual.chave:
            no_atual.esq = self._remover_recursivo(no_atual.esq, chave)
        elif chave > no_atual.chave:
            no_atual.dir = self._remover_recursivo(no_atual.dir, chave)
        else:
            if no_atual.esq is None: return no_atual.dir
            elif no_atual.dir is None: return no_atual.esq
            temp = self._minimo(no_atual.dir)
            no_atual.chave, no_atual.signi = temp.chave, temp.signi
            no_atual.dir = self._remover_recursivo(no_atual.dir, temp.chave)
        return no_atual
    
    def _minimo(self, no_atual):
        while no_atual.esq is not None: no_atual = no_atual.esq
        return no_atual

    # Altura da árvore
    def altura(self):
        return self._altura_recursiva(self.raiz)
    
    def _altura_recursiva(self, no_atual):
        if no_atual is None: return 0
        return 1 + max(self._altura_recursiva(no_atual.esq), self._altura_recursiva(no_atual.dir))

    # Número de itens
    def numero_itens(self):
        return self.tamanho

    # --- BALANCEAMENTO ---
    def balancear_arvore(self):
        nos = []
        self._guardar_nos_em_ordem(self.raiz, nos)
        self.raiz = self._construir_balanceada(nos, 0, len(nos) - 1)

    def _guardar_nos_em_ordem(self, no_atual, nos):
        if no_atual is not None:
            self._guardar_nos_em_ordem(no_atual.esq, nos)
            nos.append(no_atual)
            self._guardar_nos_em_ordem(no_atual.dir, nos)

    def _construir_balanceada(self, nos, inicio, fim):
        if inicio > fim: return None
        meio = (inicio + fim) // 2
        no = nos[meio]
        no.esq = self._construir_balanceada(nos, inicio, meio - 1)
        no.dir = self._construir_balanceada(nos, meio + 1, fim)
        return no

# TESTE
dicionario = Dicionario()
dicionario.inserir("Python", "Linguagem de programação")
dicionario.inserir("Algoritmo", "Passos para resolver um problema")
dicionario.inserir("Erro", "Erro no código")

dicionario.balancear_arvore() 

print("Lista:")
dicionario.listar()
print(f"Altura: {dicionario.altura()}")
print(f"Itens: {dicionario.numero_itens()}")