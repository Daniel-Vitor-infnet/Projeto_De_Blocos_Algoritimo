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

@cython.boundscheck(False)
@cython.wraparound(False)
cdef void fundir_duas_listas(long[:] src, long[:] dst, long esq, long meio, long dir) noexcept nogil:
    cdef long i = esq
    cdef long j = meio
    cdef long k = esq

    while i < meio and j < dir:
        if src[i] <= src[j]:
            dst[k] = src[i]
            i += 1
        else:
            dst[k] = src[j]
            j += 1
        k += 1

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
    cdef long n = dados.shape[0]
    cdef long[:] buffer = np.empty(n, dtype=np.int64)
    cdef long[:] src = dados
    cdef long[:] dst = buffer
    cdef long[:] temp
    
    cdef long step = n // num_listas_k
    cdef long num_merges, m, esq, meio, dir, i
    
    cdef int num_threads_env = int(os.environ.get("OMP_NUM_THREADS", "4"))
    
    cdef bint array_trocado = False

    print(f"Iniciando K-way merge com {num_threads_env} thread(s)...")
    start_time = time.perf_counter()

    while step < n:
        num_merges = n // (2 * step)
        
        for m in prange(num_merges, nogil=True, num_threads=num_threads_env):
            esq = m * 2 * step
            meio = esq + step
            dir = esq + 2 * step
            
            if dir > n:
                dir = n
                
            fundir_duas_listas(src, dst, esq, meio, dir)
            
        if (num_merges * 2 * step) < n:
            esq = num_merges * 2 * step
            for i in range(esq, n):
                dst[i] = src[i]

        temp = src
        src = dst
        dst = temp
        
        # inverção da flag toda vez que ocorre uma troca
        array_trocado = not array_trocado
        
        step *= 2

    end_time = time.perf_counter()
    print(f"Tempo do Merge: {end_time - start_time:.4f} segundos")

    if array_trocado:
        for i in range(n):
            dados[i] = src[i]