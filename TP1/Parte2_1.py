import time

# É um pythom muito simples de leitura sem invetar muito como verificar se o arquivo exit etc..
lista_original = open("TP1/Arquivos/lista_arquivos.txt").read().splitlines()

# Um print apenas de teste
print(f"Total: {len(lista_original)} arquivos.")
print(lista_original[:5]) 
print()

# Vou tratar todos como pior caso
""" Parte 3-2.Big O: A complexidadeé O(n^2) pq tem um loop dentro de outro automaticamente as operações crescem ao quadrado
Como são 30 mil arquivos basta fazer 30_000 x 30_000 = 900_000_000. Meu código tem um if de troca, porém vou considerar o pior caso todos fora de ordem.
Obs: inportante como eu fiz o "teve_troca" então o melhor caso seria O(n)
"""
def bubble_sort(lista):
    t = len(lista)
    passos = 0
    for i in range(t):
        teve_troca = False
        for j in range(0, t - i -1):
            passos +=1
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                teve_troca = True
        if not teve_troca:
            break
                
           
    print(f"Os passos dados foram {passos}")
    print(f"lista: {lista[:5]}")

lista_bubble = lista_original.copy()
timeI_bubble_sort = time.time()
bubble_sort(lista_bubble)
timeF_bubble_sort = time.time()
print(f"Tempo de execução do bubble_sort foi de {timeF_bubble_sort - timeI_bubble_sort}")
print()



"""  Diferente de outros algoritimos o selection sort n tem o melhor caso, mesmo que a lista esteja ordenada ele vai percorrer todos itens.
Numero de comparação é sempre constante curva quadradica
""" 
def selection_sort(lista):
    t = len(lista)
    passos = 0
    
    for idx_atual in range(t):
        index_min = idx_atual
        
        for proximo_idx in range(idx_atual + 1, t):
            passos += 1
            if lista[proximo_idx] < lista[index_min]:
                index_min = proximo_idx
        
        if index_min != idx_atual:
            lista[idx_atual], lista[index_min] = lista[index_min], lista[idx_atual]
            
    print(f"Os passos dados foram {passos}")
    print(f"lista: {lista[:5]}")
            


lista_selection = lista_original.copy()
timeI_selection = time.time()
selection_sort(lista_selection)
timeF_selection = time.time()
print(f"Tempo de execução do selection_sort foi de {timeF_selection - timeI_selection}")
print()



""" O pior caso tb é O(n^2)  melhor caso O(n) isso acontece pq quando ele acha o local do elemento ele para de buscar por essa posição 
"""
def insertion_sort(lista):
    t = len(lista)
    passos = 0
    
    for i in range(1, t):
        chave = lista[i]
        j = i - 1
        
        while j >= 0:
            passos += 1
            if lista[j] > chave:
                lista[j + 1] = lista[j]
                j -= 1
            else:
                break
        
        lista[j + 1] = chave
            
    print(f"Os passos dados foram {passos}")
    print(f"lista: {lista[:5]}")

lista_insertion = lista_original.copy()
timeI_insertion = time.time()
insertion_sort(lista_insertion)
timeF_insertion = time.time()
print(f"Tempo de execução do insertion_sort foi de {timeF_insertion - timeI_insertion}")
print()

""" Os graficos estão em TP1\Documentação\Graficos\Parte2_1
O relatorio final:
O bublle sort faz trocas com elementos ao lado. Sempre o maior elemento vai para o final de cada interação é
 é pior em grandes quantidades por causa da quantidade de trocas.
 
O selection sort seleciona o menor elemento e coloca na posição correta. Sua vantagem é pq tem baixo custo de escrita na memoria mesmo que o
número de comparações seja alto.

O inserction sort acabando sendo mais eficiente pq a cada avanço ele já deixa a parte da esquerda da lista organizada e 
só vai fazer a trocar se o elemento for maior
"""