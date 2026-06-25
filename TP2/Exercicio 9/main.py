import numpy as np
import time
import os
import exercicio9

def main():
    # Matriz dinâmica aleatória
    print("Gerando a matriz gigante de 10.000 x 10.000 ")
    matriz_original = np.random.randint(0, 200, size=(10000, 10000), dtype=np.int32)
    
    brilho = 50
    
    # Copias das matrizes para as medições
    matriz_seq = matriz_original.copy()
    matriz_paralela = matriz_original.copy()

    # Sequencial
    print("\n[Execução Sequencial - 1 thread]")
    start_seq = time.perf_counter()
    exercicio9.ajusta_brilho(matriz_seq, brilho, num_threads=1)
    end_seq = time.perf_counter()
    
    tempo_seq = end_seq - start_seq
    print(f"Tempo: {tempo_seq:.4f} segundos")

    # Paralela
    num_threads_env = int(os.environ.get("OMP_NUM_THREADS", "4"))
    print(f"\n[Execução Paralela - {num_threads_env} threads]")
    
    start_par = time.perf_counter()
    exercicio9.ajusta_brilho(matriz_paralela, brilho, num_threads=num_threads_env)
    end_par = time.perf_counter()
    
    tempo_par = end_par - start_par
    print(f"Tempo: {tempo_par:.4f} segundos")

    # Comparativo final
    if tempo_par > 0:
        speedup = tempo_seq / tempo_par
        print(f"\nA versão paralela foi {speedup:.2f}x mais rápida!")

if __name__ == "__main__":
    main()