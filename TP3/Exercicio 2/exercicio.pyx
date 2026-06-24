import cython
from cython.parallel import prange
import time
import os
import numpy as np

""" 
Vou usar o 'prange' simulando a árvore de Divisão e Conquista.
O 'prange' atua como o '#pragma omp parallel for'

- False Sharing: Evitado porque cada thread trabalha em fatias grandes e exclusivas do array.
- Load Balancing: Naturalmente equilibrado, pois no k-way cada thread funde 
  listas exatamente do mesmo tamanho.
"""

# Captura o número de threads passadas via variável de ambiente
num_threads_env = int(os.environ.get("OMP_NUM_THREADS", "4"))

# Função em C puro para fazer o merge de dois blocos (GIL desligado)
@cython.boundscheck(False)
@cython.wraparound(False)
cdef void fundir_duas_listas(long[:] src, long[:] dst, long esq, long meio, long dir) noexcept nogil:
    cdef long i = esq
    cdef long j = meio
    cdef long k = esq

    # Intercala os elementos da metade esquerda e direita
    while i < meio and j < dir:
        if src[i] <= src[j]:
            dst[k] = src[i]
            i += 1
        else:
            dst[k] = src[j]
            j += 1
        k += 1

    # Copia o que sobrou
    while i < meio:
        dst[k] = src[i]
        i += 1
        k += 1

    while j < dir:
        dst[k] = src[j]
        j += 1
        k += 1

@cython.boundscheck(False)
@cython.wraparound(False)
def parallel_kway_merge(long[:] dados, long num_listas_k):
    # Setup de variáveis tipadas pro Cython rodar rápido
    cdef long n = dados.shape[0]
    cdef long[:] buffer = np.empty(n, dtype=np.int64)
    cdef long[:] src = dados
    cdef long[:] dst = buffer
    cdef long[:] temp
    
    # Define o tamanho de cada lista inicial
    cdef long tamanho_bloco = n // num_listas_k
    cdef long step = tamanho_bloco
    
    # Variáveis do loop C
    cdef long num_merges, m, esq, meio, dir
    cdef long i

    print(f"Iniciando K-way merge com {num_threads_env} thread(s).....")
    start_time = time.time()

    # Montando a árvore de Merge (passagens)
    # Equivalente ao: 16 listas -> 8 -> 4 -> 2 -> 1
    while step < n:
        num_merges = n // (2 * step)
        
        # AQUI ENTRA O OPENMP!
        for m in prange(num_merges, nogil=True, num_threads=num_threads_env):
            esq = m * 2 * step
            meio = esq + step
            dir = esq + 2 * step
            
            # Proteção caso a divisão não seja exata no final
            if dir > n:
                dir = n
                
            fundir_duas_listas(src, dst, esq, meio, dir)
            
        # Trata a cauda do array (caso sobrem elementos fora dos pares)
        if (num_merges * 2 * step) < n:
            esq = num_merges * 2 * step
            for i in range(esq, n):
                dst[i] = src[i]

        # Swap: o destino desta rodada vira a origem da próxima
        temp = src
        src = dst
        dst = temp
        
        step *= 2

    end_time = time.time()
    print(f"Tempo de execução do Merge: {end_time - start_time:.4f} segundos")

    # Garante que o array final atualizado seja o original
    if src is not dados:
        for i in range(n):
            dados[i] = src[i]