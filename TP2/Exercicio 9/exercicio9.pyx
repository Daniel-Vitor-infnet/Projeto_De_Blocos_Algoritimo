import cython
from cython.parallel import prange

# Desliga as travas de segurança do Python para a matriz ser acessada na velocidade do C
@cython.boundscheck(False)
@cython.wraparound(False)
def ajusta_brilho(int[:, :] matriz, int brilho, int num_threads):
    
    cdef int i, j
    cdef int linhas = matriz.shape[0]
    cdef int colunas = matriz.shape[1]
    

    for i in prange(linhas, nogil=True, num_threads=num_threads):
        for j in range(colunas):
            matriz[i, j] += brilho
            
            # Trava o valor em 255 (limite máximo de brilho de um pixel)
            if matriz[i, j] > 255:
                matriz[i, j] = 255