class Fila:
    def __init__(self):
        self.itens = []
    
    def enfileirar(self, item):
        self.itens.append(item)
    
    def vazia(self):
       return len(self.itens) == 0
    
    def desenfileirar(self):
        if not self.vazia():
            return self.itens.pop(0)
        else:
            raise IndexError("A fila está vazia.")
   
    
    def tamanho(self):
        return len(self.itens)
    
    def buscar(self, p):
        indice = p - 1
        
        if 0 <= indice < len(self.itens):
            return print(f'O item é "{self.itens[indice]}"')
        else:
            return f"Posição {p} não encontrada."
        
    def imprimir(self):
        print(self.itens)