import cython
from cython.parallel import prange

# Desativamos verificações do Python para o código rodar na velocidade do C
@cython.boundscheck(False)
@cython.wraparound(False)
def ajusta_brilho(int[:, :] matriz, int brilho, int num_threads):
    cdef int i, j
    cdef int linhas = matriz.shape[0]
    cdef int colunas = matriz.shape[1]
    
    # O loop externo é distribuído entre as threads usando prange
    for i in prange(linhas, nogil=True, num_threads=num_threads):
        # O loop interno é percorrido normalmente por cada thread em suas respectivas linhas
        for j in range(colunas):
            matriz[i, j] += brilho
            
            # Trava o valor em 255 (limite do pixel)
            if matriz[i, j] > 255:
                matriz[i, j] = 255