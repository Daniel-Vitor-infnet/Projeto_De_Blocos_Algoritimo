class HashTable:
    # Vou usar armario pq faz mais sentido pra mim
    # Vou chamar de gaveta (lógica do armario)
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.armario = [[] for _ in range(tamanho)]
   
    # Fiz separado pois pode adicionar diferentes formas de calcular por exemplo quadratica
    def calc_hash(self, chave):
        # Eu ia usar o "abs(hash(chave))", porém para garantir que as bucas pedidas existam desisti
        return chave % self.tamanho

    #Achei que faz mais sentido fazer as buscas internas invés de em cada função fazer separado
    def _buscar_gaveta(self, chave):
        index = self.calc_hash(chave)
        return self.armario[index]

    def _buscar_item(self, gaveta, chave):
        for i, (chave_existente, _) in enumerate(gaveta):
            if chave_existente == chave:
                return i
        return None

    # Até parece redundante, porém é apenas para reaproveitar
    def buscar(self, chave):
        gaveta = self._buscar_gaveta(chave)
        index_item = self._buscar_item(gaveta, chave)
        
        if index_item is not None:
            _, valor = gaveta[index_item]
            print(f'O item é "{valor}"')
        else:
            print("O item ou gaveta n existe")
        return
        

    def add(self, chave, valor):
        gaveta = self._buscar_gaveta(chave)
        index_item = self._buscar_item(gaveta, chave)
        
        if index_item is not None:
            # Se o item existe, atualiza
            gaveta[index_item] = (chave, valor)
        else:
            # Se não existe, adiciona novo
            gaveta.append((chave, valor))
     
    # Usei o pop por causa do retorno        
    def remover(self, chave):
        gaveta = self._buscar_gaveta(chave)
        index_item = self._buscar_item(gaveta, chave)
        
        if index_item is None:
            return(print("Item ou gaveta não existem"))
        else:
            item_removido = gaveta.pop(index_item)
            print(f'Item removido com sucesso: {item_removido}')
            return 
        
        

