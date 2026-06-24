def calc_tamanho(estrutura):
    tam_total = 0
    
    for nome, conteudo in estrutura.items():
        
        # Se o conteúdo for um dicionário, significa que achamos uma subpasta!
        # Aí a mágica acontece: a função chama ela mesma para entrar nessa pasta
        
        # Se o item for um dicionpario quer dizer que é uma pasta. então chama a função recurisva (calc)
        if isinstance(conteudo, dict):
            tam_total += calc_tamanho(conteudo)
            
        # Caso n seja um dicionario apenas soma (apenas um arquivo)
        elif isinstance(conteudo, (int, float)):
            tam_total += conteudo
            
    return tam_total

sistema_arquivos = {
    "Documentos": {
        "Trabalho": {"projeto1.pdf": 500, "projeto2.pdf": 300},
        "Pessoal": {"receitas.txt": 10},
    },
    "Imagens": {
        "Ferias": {"foto1.jpg": 2000, "foto2.jpg": 3000},
        "logo.png": 150
    },
    "README.txt": 5
}

if __name__ == "__main__":
    total = calc_tamanho(sistema_arquivos)
    print("Varrendo disco.....\n")
    print(f"Tamanho total ocupado: {total} KB")