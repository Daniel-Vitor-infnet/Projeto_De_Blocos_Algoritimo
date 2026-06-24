# Ta bem simplão e sem comentarios esse n dei muita moral pq bom o outro (exercicio 6) vai ter literalmente tudo

class Node:
    def __init__(self, content):
        self.content = content
        self.next = None
        self.prev = None

class EditorDeTexto:
    def __init__(self):
        self.primeira_l = None
        self.linha_a = None

    def inserir_linha(self, text):
        novo_no = Node(text)

        if not self.primeira_l:
            self.primeira_l = novo_no
            self.linha_a = novo_no
        else:
            self.linha_a.next = novo_no
            novo_no.prev = self.linha_a
            self.linha_a = novo_no

    def imprimir(self):
        temp = self.primeira_l
        print()
        while temp:
            print(temp.content)
            temp = temp.next
        print()

if __name__ == "__main__":
    editor = EditorDeTexto()

    editor.inserir_linha('"A natureza,')
    editor.inserir_linha('dizem-nos,')
    editor.inserir_linha('É apenas o hábito..."')
    editor.inserir_linha('(Rousseau)')

    editor.imprimir()