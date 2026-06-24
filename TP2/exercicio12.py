import random
from functools import lru_cache

# Quantidade de estações
n = 20

# 3 linhas (índices 0, 1, 2)
e = [random.randint(1, 10) for _ in range(3)]  # Entrada
x = [random.randint(1, 10) for _ in range(3)]  # Saída
a = [[random.randint(1, 20) for _ in range(n)] for _ in range(3)]  # Montagem
t = [[[random.randint(1, 10) if i != j else 0 for _ in range(n-1)] for j in range(3)] for i in range(3)]  # Transferência

# Usei o @lru_cache pro código n precisa ficar recalculando tudo que já foi resolvido mais de uma vez
@lru_cache(None)
def f(linha, j):
    if j == 0:
        return e[linha] + a[linha][0], [f"Estação 1 na Linha {linha + 1}"]
    
    # Testa as 3 linhas anteriores para ver qual tem o melhor custo acumulado
    melhor_custo = float('inf')
    melhor_caminho = []
    
    for l_anterior in range(3):
        custo_ant, cam_ant = f(l_anterior, j - 1)
        
        # Soma a transferência Caso mude de linha)
        custo_total = custo_ant + t[l_anterior][linha][j-1] + a[linha][j]
        
        if custo_total < melhor_custo:
            melhor_custo = custo_total
            melhor_caminho = cam_ant + [f"Estação {j + 1} na Linha {linha + 1}"]
            
    return melhor_custo, melhor_caminho

# Calcula o tempo final para as 3 saídas
resultados = []
for i in range(3):
    custo, cam = f(i, n - 1)
    resultados.append((custo + x[i], cam + [f"Saída pela Linha {i + 1}"]))

# Pega a melhor opção entre as 3 linhas
temp_min, cam_escolhido = min(resultados, key=lambda item: item[0])

# Resultado
print(f"=== RESULTADO DA LINHA DE MONTAGEM (N={n}, 3 LINHAS) ===")
print(f"Tempo mínimo total: {temp_min} unidades de tempo")
print("\nMelhor caminho:")

for passo in cam_escolhido:
    print(f" -> {passo}")

print("\n" + "-"*40)
print(f"Entradas (e): {e}")
print(f"Saídas (x):   {x}")