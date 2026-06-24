import random
import time
import matplotlib.pyplot as plt

# Da forma que fiz o quicksort ele tem um custo de O(n log n) caso melhor/medio. Principalmente por ter gerado as listas com "random.choices".
def quicksort(lista):
    # Caso a lista tem 1 ou nenhum elemento ela já está ordenada. (apenas para evitar redundancias)
    if len(lista) <= 1:
        return lista

    # Escolher o primeiro item para começar a ordenação.
    pivo = lista[0] #Pegadinha como o pivo é fixo sempre no primeiro elemento o custo vai ser 0(n^2) mesmo que esteja ordenada

    # Dividindo a llista em 3 partes
    menores = [x for x in lista if x < pivo]
    iguais = [x for x in lista if x == pivo] # Quando a lista tem elementos repetidos. (Apenas para ser elegante)
    maiores = [x for x in lista if x > pivo]

    return quicksort(menores) + iguais + quicksort(maiores)


# Não vou considerar custo ou tempo, pois o foco é o quicksort e n uma geração de lista.
listas_aleatorias = [
    random.choices(range(1, 10001), k=t) 
    for t in range(25, 1025, 25)
]

tamanhos = []
tempos = []

for lista in listas_aleatorias:
    tamanhos.append(len(lista))
    inicio = time.perf_counter()
    quicksort(lista)
    fim = time.perf_counter()
    tempos.append(fim - inicio)
    
    print(f"{tamanhos[-1]:<20} | {tempos[-1]:.6f}")
    
    
    
    
# Sinceramente deu preguiça em fazer os gráficos, aí pesquisando essa lib "matplotlib.pyplot" que faz praticamente tudo sozinha e aproveitei ela
plt.figure(figsize=(8, 5))
plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='b')
plt.title("Tempo de Execução do QuickSort (Caso Médio)")
plt.xlabel("Tamanho da Lista (N)")
plt.ylabel("Tempo de Execução (segundos)")
plt.grid(True)
plt.show()  # Abre a janela com o gráfico pronto.