def desenhar_regua(n):
    if n == 0:
        return
    
    # Subintervalo superior
    desenhar_regua(n - 1)
    
    print('-' * n)
    
    # Subintervalo inferior
    desenhar_regua(n - 1)

print("Régua de ordem 4:")
desenhar_regua(4)