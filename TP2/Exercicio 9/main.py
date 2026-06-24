import numpy as np
import time
import os

# Importa o módulo que acabamos de compilar com o setup.py
import exercicio9

def main():
    # 1. Geração de Dados: Matriz dinâmica
    print("Gerando matriz gigante de 10.000 x 10.000...")
    # Usamos np.int32 para ficar compatível com o "int" do C no Cython
    matriz_original = np.random.randint(0, 200, size=(10000, 10000), dtype=np.int32)
    
    brilho = 50
    
    # Fazemos cópias para que um teste não altere a matriz do outro
    matriz_seq = matriz_original.copy()
    matriz_paralela = matriz_original.copy()

    # 2. Medição Sequencial (forçando 1 thread)
    print("\nIniciando processamento Sequencial (1 thread)...")
    start_seq = time.time()
    exercicio9.ajusta_brilho(matriz_seq, brilho, num_threads=1)
    end_seq = time.time()
    tempo_seq = end_seq - start_seq
    print(f"Tempo Sequencial: {tempo_seq:.4f} segundos")

    # 3. Medição Paralela
    # Pega o número de threads da variável de ambiente, ou usa 4 por padrão
    num_threads_env = int(os.environ.get("OMP_NUM_THREADS", "4"))
    print(f"\nIniciando processamento Paralelo ({num_threads_env} threads)...")
    
    start_par = time.time()
    exercicio9.ajusta_brilho(matriz_paralela, brilho, num_threads=num_threads_env)
    end_par = time.time()
    tempo_par = end_par - start_par
    print(f"Tempo Paralelo: {tempo_par:.4f} segundos")

    # 4. Resultado e Speedup
    if tempo_par > 0:
        speedup = tempo_seq / tempo_par
        print(f"\nSpeedup: A versão paralela foi {speedup:.2f}x mais rápida!")

if __name__ == "__main__":
    main()