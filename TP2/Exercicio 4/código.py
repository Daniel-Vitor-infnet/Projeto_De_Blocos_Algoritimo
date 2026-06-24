import random
import time
import matplotlib.pyplot as plt

def particao(lista, esq, dir):
    # Escolhe o último elemento como pivô
    pivo = lista[dir]
    i = esq - 1
    
    #Percorre a lista jogando os menores ou iguais ao pivo para esquerda
    for j in range(esq, dir):
        if lista[j] <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]
    #Ajusta o pivo
    lista[i + 1], lista[dir] = lista[dir], lista[i + 1]
    return i + 1

def quick_select(lista, esq, dir, k):
    if esq <= dir:
        pivo_index = particao(lista, esq, dir)
        
        #Faz a comparação do índice do pivô com k para decidir qual lado da partição processar
        if pivo_index == k:
            return lista[pivo_index]
        elif pivo_index > k:
            return quick_select(lista, esq, pivo_index - 1, k)
        else:
            return quick_select(lista, pivo_index + 1, dir, k)

listas_aleatorias = [
    random.choices(range(1, 10001), k=t) 
    for t in range(25, 1025, 25)
]

tempos = []
tamanhos = []

for lista in listas_aleatorias:
    tamanho=len(lista)
    k = tamanho // 2 
    tamanhos.append(tamanho)

    inicio = time.perf_counter()
    
    resultado = quick_select(lista, 0, tamanho - 1, k)
    
    fim = time.perf_counter()
    
    tempo_total = fim - inicio
    tempos.append(tempo_total)
    
    print(f"{tamanhos[-1]:<20} | {tempos[-1]:.6f}")

plt.figure(figsize=(8, 5))
plt.plot(tamanhos, tempos, marker='o', linestyle='-', color='b')
plt.title("Tempo de Execução do QuickSelect (Caso Médio)")
plt.xlabel("Tamanho da Lista (N)")
plt.ylabel("Tempo de Execução (segundos)")
plt.grid(True)
plt.show()
