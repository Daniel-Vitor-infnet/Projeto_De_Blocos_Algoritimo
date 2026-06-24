import time
import random

class MinHeap:
    def __init__(self):
        self.h = []
        self.c = 0

    def push(self, prio, pid, proc):
        self.c += 1
        self.h.append([prio, self.c, pid, proc])
        self.subir(len(self.h) - 1)

    def pop(self):
        if not self.h: return None
        self.h[0], self.h[-1] = self.h[-1], self.h[0]
        x = self.h.pop()
        if self.h: self.descer(0)
        return x[2], x[3]

    def subir(self, i):
        p = (i - 1) // 2
        while i > 0 and self.h[i][0] < self.h[p][0]:
            self.h[i], self.h[p] = self.h[p], self.h[i]
            i, p = p, (p - 1) // 2

    def descer(self, i):
        n = len(self.h)
        while True:
            e, d, m = 2*i + 1, 2*i + 2, i
            if e < n and self.h[e][0] < self.h[m][0]: m = e
            if d < n and self.h[d][0] < self.h[m][0]: m = d
            if m == i: break
            self.h[i], self.h[m] = self.h[m], self.h[i]
            i = m

def main():
    pronta = MinHeap()
    susp = MinHeap()
    q = 5 # Quantum
    t = 0 # Tempo global

    print(f"{'T':<4} | {'PID':<4} | {'ESTADO':<22} | {'BURST':<5} | {'MOTIVO'}")
    print("-" * 65)

    # Cria 10 processos (Nova -> Pronta)
    # Burst entre 16 e 25 garante pelo menos 4 idas na CPU (Quantum 5)
    for i in range(1, 11):
        burst = random.randint(16, 25)
        pronta.push(burst, f"P{i}", {"burst": burst, "wake": 0})
        print(f"{0:<4} | P{i:<3} | Nova -> Pronta         | {burst:<5} | Criado")

    while pronta.h or susp.h:
        # Acorda quem estava na fila Suspensa esperando I/O
        temp = []
        while susp.h:
            pid, p = susp.pop()
            if p["wake"] <= t:
                print(f"{t:<4} | {pid:<3} | Suspensa -> Pronta     | {p['burst']:<5} | Dado recebido")
                pronta.push(p["burst"], pid, p)
            else:
                temp.append((pid, p))
                
        for pid, p in temp:
            susp.push(p["wake"], pid, p)

        # CPU Ociosa
        if not pronta.h:
            t += 1
            time.sleep(0.01)
            continue

        # Pronta -> Executando
        pid, p = pronta.pop()
        print(f"{t:<4} | {pid:<3} | Pronta -> Executando   | {p['burst']:<5} | Assumiu CPU")

        # Temporiza a execução na CPU
        exec_t = min(q, p["burst"])
        for _ in range(exec_t):
            time.sleep(0.05) # Delay simulando processamento
            t += 1
        
        p["burst"] -= exec_t

        # Saída da Execução
        if p["burst"] <= 0:
            print(f"{t:<4} | {pid:<3} | Executando -> Terminada| 0     | Encerrado")
        else:
            if random.random() < 0.3: # 30% de chance de pedir um I/O
                p["wake"] = t + random.randint(2, 6) # Fica bloqueado alguns ciclos
                print(f"{t:<4} | {pid:<3} | Executando -> Suspensa | {p['burst']:<5} | I/O pendente")
                susp.push(p["wake"], pid, p)
            else:
                print(f"{t:<4} | {pid:<3} | Executando -> Pronta   | {p['burst']:<5} | Fim Quantum")
                pronta.push(p["burst"], pid, p)

if __name__ == "__main__":
    main()