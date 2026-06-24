import random
from functools import lru_cache

# Quantidade de estações
n = 20

# Gerando custos aleatórios
e = [random.randint(1, 10) for _ in range(2)]  # Entrada
x = [random.randint(1, 10) for _ in range(2)]  # Saída
a = [[random.randint(1, 20) for _ in range(n)] for _ in range(2)]  # Montagem
t = [[random.randint(1, 10) for _ in range(n - 1)] for _ in range(2)]  # Transferência

# Usei o @lru_cache pro código n precisa ficar recalculando tudo que já foi resolvido mais de uma vez
@lru_cache(None)
def f(linha, j):
    if j == 0:
        # Custo e o caminho inicializado
        return e[linha] + a[linha][0], [f"Estação 1 na Linha {linha + 1}"]
    
    linha_oposta = 1 - linha
    
    # Custo e caminho para manter na mesma linha
    custo_manter, cam_manter = f(linha, j - 1)
    
    # Custo e caminho para trocar de linha
    custo_trocar, cam_trocar = f(linha_oposta, j - 1)
    custo_trocar += t[linha_oposta][j - 1] # soma a transferência
    
    # Decide qual é amelhor escolha 
    if custo_manter <= custo_trocar:
        custo_total = a[linha][j] + custo_manter
        cam_atual = cam_manter + [f"Estação {j + 1} na Linha {linha + 1}"]
    else:
        custo_total = a[linha][j] + custo_trocar
        cam_atual = cam_trocar + [f"Estação {j + 1} na Linha {linha + 1}"]
        
    return custo_total, cam_atual

# Calcula o tempo final para as duas saídas possíveis
custo_l1, cam_l1 = f(0, n - 1)
temp_final_l1 = custo_l1 + x[0]

custo_l2, cam_l2 = f(1, n - 1)
temp_final_l2 = custo_l2 + x[1]

# Escolhe o menor tempo global e o respectivo caminho
if temp_final_l1 <= temp_final_l2:
    temp_min = temp_final_l1
    cam_escolhido = cam_l1 + ["Saída pela Linha 1"]
else:
    temp_min = temp_final_l2
    cam_escolhido = cam_l2 + ["Saída pela Linha 2"]

# Resultado
print(f"=== RESULTADO DA LINHA DE MONTAGEM (N={n}) ===")
print(f"Tempo mínimo total: {temp_min} unidades de tempo")
print("\nMelhor caminho:")

for passo in cam_escolhido:
    print(f" -> {passo}")

print("\n" + "-"*40)
print(f"Custos de Entrada (e): Linha 1: {e[0]} | Linha 2: {e[1]}")
print(f"Custos de Saída (x):   Linha 1: {x[0]} | Linha 2: {x[1]}")