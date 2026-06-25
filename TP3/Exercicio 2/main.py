import numpy as np
import os
import sys
from exercicio import parallel_kway_merge

def main():
    threads = os.environ.get("OMP_NUM_THREADS", "4")
    print(f"--- Testando com {threads} threads ---")

    # Arquivo na mesma pasta do script
    caminho_txt = "lista_arquivos.txt"
    
    try:
        with open(caminho_txt, 'r') as f:
            linhas = f.read().splitlines()
    except FileNotFoundError:
        print(f"Arquivo '{caminho_txt}' não encontrado na pasta atual!")
        sys.exit()

    tamanhos_hash = [abs(hash(linha)) % 1000000 for linha in linhas]
    dados_base = np.array(tamanhos_hash, dtype=np.int64)
    
    K = 16 
    dados = np.tile(dados_base, K) 
    
    tamanho_por_lista = len(dados_base)
    print(f"Massa de dados carregada: {len(dados)} números baseados no arquivo do TP1.")

    for i in range(K):
        inicio = i * tamanho_por_lista
        fim = inicio + tamanho_por_lista
        dados[inicio:fim].sort()

    print("Sub-listas pré-ordenadas. Mandando pro Cython fazer a árvore de merge...")
    
    parallel_kway_merge(dados, K)

    esta_ordenado = np.all(dados[:-1] <= dados[1:])
    if esta_ordenado:
        print("Sucesso! O array final está perfeitamente ordenado.")
    else:
        print("Deu ruim na ordenação.")

if __name__ == "__main__":
    main()