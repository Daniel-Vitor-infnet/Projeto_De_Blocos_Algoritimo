import cython
from cython.parallel import prange
import time
import os

""" Vou usar o cython dessa forma pq foi a forma que o Tiago passou e eu gostei
Vou usar o "prange" para paralelizar o loop e n precisar usar o "pragma" e "reduction(+:sum)"
"""
# Captura o número de threads passadas
num_threads_env = int(os.environ.get("OMP_NUM_THREADS", "1"))

# variáveis declaradas
num_passos = cython.declare(cython.long, 100000000)
passo = cython.declare(cython.double, 1.0 / num_passos)
soma = cython.declare(cython.double, 0.0)
x = cython.declare(cython.double, 0.0)
i = cython.declare(cython.long, 0)

print(f"Iniciando cálculo com {num_threads_env} thread(s).....")

start_time = time.time()

# A redução da variável 'soma' e a privacidade de 'x' e 'i'
for i in prange(num_passos, nogil=True, num_threads=num_threads_env):
    x = (i + 0.5) * passo
    soma += 4.0 / (1.0 + x * x)

end_time = time.time()

# Cálculo final
pi = passo * soma

print(f"Pi calculado: {pi}")
print(f"Tempo de execução: {end_time - start_time} segundos")