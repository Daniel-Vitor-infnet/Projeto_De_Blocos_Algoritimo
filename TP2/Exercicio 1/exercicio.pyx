import cython
from cython.parallel import prange
import time
import os

def calcular_pi():
    # Pega o valor em um objeto Python 
    threads_py = int(os.environ.get("OMP_NUM_THREADS", "1"))
    
    # Converte para C
    num_threads_env = cython.declare(cython.int, threads_py)

    # variáveis declaradas em C
    num_passos = cython.declare(cython.long, 100000000)
    passo = cython.declare(cython.double, 1.0 / num_passos)
    soma = cython.declare(cython.double, 0.0)
    x = cython.declare(cython.double, 0.0)
    i = cython.declare(cython.long, 0)

    print(f"Iniciando cálculo com {num_threads_env} thread(s).....")

    start_time = time.perf_counter()

    for i in prange(num_passos, nogil=True, num_threads=num_threads_env):
        x = (i + 0.5) * passo
        soma += 4.0 / (1.0 + x * x)

    end_time = time.perf_counter()

    # Cálculo final
    pi = passo * soma

    print(f"Pi calculado: {pi}")
    print(f"Tempo de execução: {end_time - start_time:.4f} segundos")

if __name__ == "__main__":
    calcular_pi()