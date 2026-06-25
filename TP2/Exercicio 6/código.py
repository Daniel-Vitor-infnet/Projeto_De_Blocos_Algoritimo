import os

class Node:
    def __init__(self, content):
        self.content = content
        self.next = None
        self.prev = None

class EditorDeTexto:
    def __init__(self):
        self.primeira_l = None
        self.linha_a = None  # Ponteiro C (corrente)

    #Move o ponteiro linha_a para a linha de número 'n'
    def ir_para_linha(self, n):
        if n <= 0:
            return
        
        temp = self.primeira_l
        contador = 1
        
        # Percorre a lista até achar a linha n ou chegar ao fim
        while temp and contador < n:
            temp = temp.next
            contador += 1
            
        if temp:
            self.linha_a = temp
            
    #  Se 'n' for fornecido vai para a linha 'n' antes de inserir
    def comando_inserir(self, text, n=None):
        if n is not None:
            self.ir_para_linha(n)

        novo_no = Node(text)

        if not self.primeira_l:
            self.primeira_l = novo_no
            self.linha_a = novo_no
        else:
            # caso a inserção seja no meio do texto
            novo_no.next = self.linha_a.next
            novo_no.prev = self.linha_a
            
            if self.linha_a.next: # Se houver uma linha depois da atual, ela aponta para a nova
                self.linha_a.next.prev = novo_no
                
            self.linha_a.next = novo_no
            self.linha_a = novo_no # A linha corrente

    def imprimir(self):
        temp = self.primeira_l
        contador = 1
        print("\n--- Texto Atual ---")
        while temp:
            # Coloquei um contador de linha só para ficar melhor apresentavel
            print(f"{contador} | {temp.content}")
            temp = temp.next
            contador += 1
        print("-------------------\n")
        

    # Exclui as linhas da posição i até f (Caso nada seja passoado irá excluir a linha corrente) 
    def comando_excluir(self, i=None, f=None):
        if not self.primeira_l:
            return

        # Defini quem é o primeiro e o último nó a serem excluídos
        if i is None and f is None:
            no_inicio = self.linha_a
            no_fim = self.linha_a
        else:
            # Encontra o nó inicial (i)
            no_inicio = self.primeira_l
            contador = 1
            while no_inicio and contador < i:
                no_inicio = no_inicio.next
                contador += 1
            
            if not no_inicio: return 
            
            # Encontra o nó final (f) a partir do inicial
            no_fim = no_inicio
            while no_fim and contador < f:
                if no_fim.next:
                    no_fim = no_fim.next
                contador += 1

        # Ponte entre o que vem antes de 'i' e depois de 'f'
        no_anterior = no_inicio.prev
        no_proximo = no_fim.next

        if no_anterior:
            no_anterior.next = no_proximo
        else:
            self.primeira_l = no_proximo

        if no_proximo:
            no_proximo.prev = no_anterior

        # Atualizar o ponteiro da linha corrente (linha_a)
        if no_proximo:
            self.linha_a = no_proximo
        elif no_anterior:
            self.linha_a = no_anterior
        else:
            self.linha_a = None # O texto todo foi apagado
            
            
    def comando_duplicar(self, i, f, p):
        if not self.primeira_l:
            return

        # Coleta os conteúdos das linhas de i a f
        conteudos_copiados = []
        no_atual = self.primeira_l
        contador = 1

        # Navega até a linha i
        while no_atual and contador < i:
            no_atual = no_atual.next
            contador += 1

        if not no_atual: 
            return 

        # Copia os conteúdos de i até f
        while no_atual and contador <= f:
            conteudos_copiados.append(no_atual.content)
            no_atual = no_atual.next
            contador += 1

        if not conteudos_copiados:
            return

        # linha 'p' (alvo)
        no_alvo = self.primeira_l
        contador = 1
        while no_alvo and contador < p:
            no_alvo = no_alvo.next
            contador += 1

        if not no_alvo:
            return

        # Inserir os nós copiados logo após a linha 'p'
        for texto in conteudos_copiados:
            novo_no = Node(texto)
            
            # Encaixa o novo_no logo após o no_alvo
            novo_no.next = no_alvo.next
            novo_no.prev = no_alvo
            
            if no_alvo.next:
                no_alvo.next.prev = novo_no
                
            no_alvo.next = novo_no
            
            no_alvo = novo_no
            
        # Atualiza a linha corrente para a última linha duplicada
        self.linha_a = no_alvo
        
        
    def comando_listar(self, i=None, f=None):
        if not self.primeira_l:
            print("O texto está vazio.")
            return

        temp = self.primeira_l
        contador = 1

        print("\n--- Listagem do Texto ---")
        
        # Caso n tenha paramentros lista tudo
        if i is None and f is None:
            while temp:
                print(f"{contador} ->| {temp.content}")
                temp = temp.next
                contador += 1
        else:
            # Navega até a linha 'i'(sem imprimir)
            while temp and contador < i:
                temp = temp.next
                contador += 1
            
            # Imprime a partir da linha 'i' até chegar na linha 'f'
            while temp and contador <= f:
                print(f"{contador} ->| {temp.content}")
                temp = temp.next
                contador += 1
                
    def comando_salvar(self, arq, i=None, f=None):
        if not self.primeira_l:
            print("O texto está vazio. Nada para salvar.")
            return

        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.join(diretorio_atual, arq)

        try:
            with open(caminho_completo, 'w', encoding='utf-8') as arquivo:
                temp = self.primeira_l
                contador = 1

                if i is None and f is None:
                    # Se não passou i e f, salva o texto todo
                    while temp:
                        arquivo.write(temp.content + '\n')
                        temp = temp.next
                else:
                    # Navega até a linha 'i'
                    while temp and contador < i:
                        temp = temp.next
                        contador += 1
                    
                    # Salva as linhas de 'i' até 'f'
                    while temp and contador <= f:
                        arquivo.write(temp.content + '\n')
                        temp = temp.next
                        contador += 1
                        
            print(f"Sucesso: Texto salvo em '{caminho_completo}'.")
            
        except Exception as erro:
            print(f"Ocorreu um erro ao tentar salvar o arquivo: {erro}")
            
    def comando_alterar(self, novo_texto, n=None):
        if not self.primeira_l:
            print("O texto está vazio. Não há o que alterar.")
            return

       
        if n is not None:
            self.ir_para_linha(n)

        # Só substitui o conteúdo do nó atual
        if self.linha_a:
            self.linha_a.content = novo_texto
                

# --- TESTANDO O CÓDIGO ---
if __name__ == "__main__":
    editor = EditorDeTexto()

    print("1. Inserindo linhas iniciais:")
    editor.comando_inserir('"A natureza,')
    editor.comando_inserir('dizem-nos,')
    editor.comando_inserir('(Rousseau)')
    editor.comando_inserir('Excluir A')
    editor.comando_inserir('Excluir B')
    editor.comando_inserir('Excluir C (vai sobrar)')
    editor.comando_inserir('Duplicar A')
    editor.comando_inserir('Duplicar B')
    editor.comando_inserir('Duplicar C')
    
    editor.imprimir()

    print("2. Excluindo linhas 4 a 5:")
    editor.comando_excluir(4, 5)
    editor.imprimir()
    
    print("3. Duplicando as linhas 5 a 7 para a 3 posição")
    editor.comando_duplicar(5, 7, 3)
    editor.imprimir()
    
    print("4. Listando linhas 2 a 6:")
    editor.comando_listar(2, 6)
    
    print("5. Listando todo o texto:")
    editor.comando_listar()
    
    
    print()
    print("6. Salvando o texto completo e depois só os trechos 2 a 6:")
    editor.comando_salvar("texto_Rousseau_completo.txt")
    editor.comando_salvar("texto_Rousseau_trechos.txt", 2, 6)
    
    print()
    print("7. Alterando a linha 7 para 'Apenas edição':")
    editor.comando_alterar("Apenas edição", 7)
    editor.imprimir()
    