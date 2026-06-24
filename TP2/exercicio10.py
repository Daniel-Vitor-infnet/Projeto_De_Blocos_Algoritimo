import asyncio
import random

async def sensor(fila: asyncio.Queue):
    # Gera batimentos cardíacos aleatórios entre 40 e 180 bpm a cada 0.5 segundos
    try:
        while True:
            # Gera um batimento
            batimento = random.randint(40, 180)
            # Espera caso a fila esteja cheia
            await fila.put(batimento)
            # Simula o tempo de batimento
            await asyncio.sleep(0.5)
            
    except asyncio.CancelledError: # Tratamento caso a tarefa seja cancelada
        print("Sensor: Sensor de batimentos desligado.")

async def monitor(fila: asyncio.Queue):
    # ABnaliza cada batimento da fila e faz o tratamento
    try:
        while True:
            batimento = await fila.get()
            
            # Verifica se o batimento é perigoso
            if batimento > 120:
                print(f"AViso: Batimento em {batimento}!")
            else:
                print(f"Normal: {batimento}")
                
                
            fila.task_done()
            
    except asyncio.CancelledError:# Tratamento caso a tarefa seja cancelada
        print("Monitor: Monitor médico desligado.")

async def main():
    print("Iniciando Sistema de Monitoramento Hospitalar...\n")
    
    fila = asyncio.Queue(maxsize=10)
    
    # Inicia as duas corrotinas simultaneamente
    tarefa_sensor = asyncio.create_task(sensor(fila))
    tarefa_monitor = asyncio.create_task(monitor(fila))
    
    # Encerramento Elegante
    await asyncio.sleep(10)
    
    print("\n*** Encerrando o sistema... ***")
    
    # Finaliza as tarefas em loop
    tarefa_sensor.cancel()
    tarefa_monitor.cancel()
    
    await asyncio.gather(tarefa_sensor, tarefa_monitor, return_exceptions=True)
    
    print("==================================================")
    print("Sistema de monitoramento encerrado com sucesso.")

if __name__ == "__main__":
    asyncio.run(main())