class Pilha:
    def __init__(self):
        self.itens = []
        
    def vazia(self):
        return len(self.itens) == 0
    
    def empilhar(self, item):
        self.itens.append(item)
    
    def desempilhar(self):
        if not self.vazia():
            return self.itens.pop()
        else:
            return None
    
    def topo(self):
        if not self.vazia():
            return self.itens[-1]
        else:
            return None
    
    
    def buscar(self, p):

        indice = p - 1
        
        if 0 <= indice < len(self.itens):
            return print(f'O item é "{self.itens[indice]}"')
        else:
            return f"Posição {p} não encontrada."
    
    def imprimir(self):
        print(self.itens)
        
    