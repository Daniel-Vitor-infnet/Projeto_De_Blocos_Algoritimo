# --- DADOS DE ENTRADA ---
CAPACIDADE_SERVIDOR = 100 # GB de RAM máxima por servidor

# Lista com os requisitos de RAM de cada uma das 60 VMs solicitadas
VMS_SOLICITADAS = [
    48, 12, 35, 22, 17, 65, 8, 42, 53, 29,
    14, 38, 47, 19, 25, 61, 33, 9, 55, 23,
    44, 16, 50, 31, 11, 28, 58, 41, 13, 37,
    62, 21, 45, 18, 26, 52, 34, 7, 49, 20,
    39, 15, 57, 32, 12, 27, 54, 43, 10, 36,
    60, 24, 46, 16, 22, 51, 30, 8, 40, 25
]

# --- 1. HEURÍSTICA NEXT-FIT (Próximo Encaixe) ---
def heuristica_next_fit(vms, capacidade):
    servidores = []
    servidor_atual = []
    ocupacao_atual = 0

    for vm in vms:
        # Se couber no servidor atual, coloca lá
        if ocupacao_atual + vm <= capacidade:
            servidor_atual.append(vm)
            ocupacao_atual += vm
        else:
            # Se não couber, fecha o servidor atual e abre um novo
            servidores.append(servidor_atual)
            servidor_atual = [vm]
            ocupacao_atual = vm
            
    # Não esquece de adicionar o último servidor aberto
    if servidor_atual:
        servidores.append(servidor_atual)
        
    return servidores

# --- 2. HEURÍSTICA FIRST-FIT DECREASING (Primeiro Encaixe Decrescente) ---
def heuristica_first_fit_decreasing(vms, capacidade):
    # Primeiro passo: ordenar as VMs da maior para a menor
    vms_ordenadas = sorted(vms, reverse=True)
    servidores = []

    for vm in vms_ordenadas:
        alocado = False
        # Percorre os servidores já abertos
        for servidor in servidores:
            if sum(servidor) + vm <= capacidade:
                servidor.append(vm)
                alocado = True
                break # Sai do loop de servidores, pois já achou um lugar
        
        # Se não couber em nenhum servidor existente, abre um novo
        if not alocado:
            servidores.append([vm])
            
    return servidores

# --- EXECUÇÃO ---
if __name__ == "__main__":
    # Rodando as duas heurísticas
    resultado_nf = heuristica_next_fit(VMS_SOLICITADAS, CAPACIDADE_SERVIDOR)
    resultado_ffd = heuristica_first_fit_decreasing(VMS_SOLICITADAS, CAPACIDADE_SERVIDOR)

    # Coletando os dados para o relatório
    qtd_nf = len(resultado_nf)
    qtd_ffd = len(resultado_ffd)
    economia = qtd_nf - qtd_ffd

    # Formatando a saída exatamente como o enunciado pede
    print("=== RESULTADO DA ALOCAÇÃO (HEURÍSTICAS) ===")
    
    print("\n[Heurística Next-Fit]")
    print(f"- Servidores utilizados: {qtd_nf} servidores")
    soma_nf_1 = sum(resultado_nf[0])
    print(f"- Exemplo de ocupação do Servidor 1: {resultado_nf[0]} (Total: {soma_nf_1}/{CAPACIDADE_SERVIDOR} GB)")

    print("\n[Heurística First-Fit Decreasing]")
    print(f"- Servidores utilizados: {qtd_ffd} servidores")
    soma_ffd_1 = sum(resultado_ffd[0])
    print(f"- Exemplo de ocupação do Servidor 1: {resultado_ffd[0]} (Total: {soma_ffd_1}/{CAPACIDADE_SERVIDOR} GB)")

    print(f"\nConclusão: A heurística First-Fit Decreasing economizou {economia} servidores em relação à Next-Fit.")