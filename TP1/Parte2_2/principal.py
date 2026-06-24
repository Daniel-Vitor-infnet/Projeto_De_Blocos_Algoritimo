import sys
import os
import psutil
import time

# Apena para garantir que o caminho do hash esteja certo.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from hashTable import HashTable
from pilha import Pilha
from fila import Fila

# É um pythom muito simples de leitura sem invetar muito como verificar se o arquivo exit etc..
lista_original = open(os.path.join(BASE_DIR, "..", "Arquivos", "lista_arquivos.txt")).read().splitlines()

# Um print apenas de teste
print(f"Total: {len(lista_original)} arquivos.")
print(lista_original[:5]) 
print()

# Função para pegar o "print" da memória agora (em KB)
def pegar_memoria():
    processo = psutil.Process(os.getpid())
    return processo.memory_info().rss / 1024

############## HASH ##############
mem_i_hash = pegar_memoria()
tempo_i_hash = time.time()

# Como a lista tem 30 mil itens e a hash tem que ser maior para evitar colisões, vou adicionar 50% do tamanho da lista.
tamanho_hash_table = len(lista_original) * 1.5
hash_table = HashTable(int(tamanho_hash_table))

#Vou aproveitar o add e usar apenas um for.
for i, item in enumerate(lista_original):
    hash_table.add(i, item)
    
print("Buscando itens na Hash Table:")
hash_table.buscar(1)
hash_table.buscar(100)
hash_table.buscar(1000)
hash_table.buscar(5000)

hash_table.remover(1000)
hash_table.add(30001, "Arquivo_1000.txt")

mem_f_hash = pegar_memoria()
tempo_f_hash = time.time()

print(f"Hash Table Tempo: {tempo_f_hash - tempo_i_hash:.3f}s | Memória: {mem_f_hash - mem_i_hash:.2f} KB")
print()

############## PILHA ##############

mem_i_pilha = pegar_memoria()
tempo_i_pilha = time.time()
pilha = Pilha()

for item in lista_original:
    pilha.empilhar(item)
    
print("Buscando itens na Pilha:")
pilha.buscar(1)
pilha.buscar(100)
pilha.buscar(1000)
pilha.buscar(5000)

pilha.desempilhar()  # Remove o último item
pilha.empilhar("Arquito_De_Exemplo.txt")

mem_f_pilha = pegar_memoria()
tempo_f_pilha = time.time()

print(f"Pilha Tempo: {tempo_f_pilha - tempo_i_pilha:.3f}s | Memória: {mem_f_pilha - mem_i_pilha:.2f} KB")
print()


############## FILA ##############

mem_i_fila = pegar_memoria()
tempo_i_fila = time.time()
fila = Fila()
for item in lista_original:
    fila.enfileirar(item)
    
print("Buscando itens na Fila:")
fila.buscar(1)  
fila.buscar(100)
fila.buscar(1000)
fila.buscar(5000)

fila.desenfileirar()  # Remove o primeiro item
fila.enfileirar("Arquito_De_Exemplo.txt")

mem_f_fila = pegar_memoria()
tempo_f_fila = time.time()

print(f"Fila Tempo: {tempo_f_fila - tempo_i_fila:.3f}s | Memória: {mem_f_fila - mem_i_fila:.2f} KB")

""" Graficos em TP1\Documentação\Graficos\Parte2_2
Relatorio final:
O hash foi oq mais consumiu mémoria. Isso acontece pq o c´digo pré aloca 30mil gavetas +50% e 
o tempo tb foi maior devido aos cáculos usados.

A pilha e a fila tem tempos e mémorias bem parecidos, isso acontece pq ambos tem uma 
estrutura de lista simples.

EM todas estruturas foi de O(1) para adicionar, buscar e remover.
"""