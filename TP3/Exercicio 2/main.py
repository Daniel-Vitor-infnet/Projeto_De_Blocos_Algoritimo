import numpy as np
import os
from exercicio import parallel_kway_merge

# Força o número de threads
os.environ["OMP_NUM_THREADS"] = "8"

K = 16 # Número de listas iniciais (como pede o enunciado)
TAMANHO_POR_LISTA = 500000 
TAMANHO_TOTAL = K * TAMANHO_POR_LISTA

print(f"Gerando dados ({TAMANHO_TOTAL} números)...")
dados = np.random.randint(0, 1000000, size=TAMANHO_TOTAL, dtype=np.int64)

# Como é K-way é preciso simular que as K listas individuais já vieram ordenadas
for i in range(K):
    inicio = i * TAMANHO_POR_LISTA
    fim = inicio + TAMANHO_POR_LISTA
    dados[inicio:fim].sort()

print("K-listas ordenadas individualmente. Rodando o Cython...")

parallel_kway_merge(dados, K)

# Verifica a ordenação final
esta_ordenado = np.all(dados[:-1] <= dados[1:])
print(f"O array final está perfeitamente ordenado? {esta_ordenado}")