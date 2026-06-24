import asyncio
import random
import time


async def baixar_arquivo(nome_arquivo):
    print(f" Iniciando download (s): {nome_arquivo}")

    # f. Fiz o if logo de cara para nosso "virus" ksks
    if nome_arquivo == "virus.exe":
        await asyncio.sleep(2)  # Fiz um tempo simulado só pra dar um charme
        raise ValueError(
            f"Download abortado: '{nome_arquivo}' é um arquivo malicioso!")

    # b. Simulação de I/O (tempo aleatório)
    tempo_rede = random.uniform(1, 15)
    await asyncio.sleep(tempo_rede)

    # c. Logs de Status
    print(f"✅ Concluído: {nome_arquivo} (levou {tempo_rede:.2f}s)")
    return nome_arquivo


async def main():
    # Lista com mais de 5 arquivos, incluindo o arquivo problemático
    arquivos_para_baixar = [
        "Rainbow_Six_Siege.exe",
        "Arena_Breakout.exe",
        "Steam_Launcher.lnk",
        "Top_Gun_Maverick.mp4",
        "1883_Season1.mkv",
        "virus.exe",
        "Counter_Strike_2.exe",
        "Yellowstone_Ep01.avi",
        "Ready_or_Not.exe"
    ]

    print("Iniciando Gerenciador de Downloads...\n")
    temp_i = time.time()

    # lista de corrotinas
    tarefas = [baixar_arquivo(arquivo) for arquivo in arquivos_para_baixar]

    # d. Execução Concorrente 
    # f. Tratamento de exceções
    resultados = await asyncio.gather(*tarefas, return_exceptions=True)

    temp_f = time.time()

    # e. Relatório Final
    arq_sucesso = []

    print("\n--- Processando Resultados ---")
    for resultado in resultados:
        # Verifica se o resultado for uma exceção (caso do virus.exe)
        if isinstance(resultado, Exception):
            print(f"❌ Falha registrada: {resultado}")
        else:
            arq_sucesso.append(resultado)

    print("\n================ Downloads Concluídos ================")
    print(f"Arquivos baixados com sucesso: {arq_sucesso}")
    print(f"Tempo total de execução: {temp_f - temp_i:.2f} segundos")
    print("=========================================================")

if __name__ == "__main__":
    asyncio.run(main())
