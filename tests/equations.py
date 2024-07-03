def mapValues(valor_atual: int, max_atual: int) -> float:
    novo_max = 100
    novo_min = 0
    min_atual = 0
    # Calcula o novo valor mapeado para o novo intervalo
    novo_valor = (valor_atual - min_atual) * (novo_max - novo_min) / (max_atual - min_atual) + novo_min
    return novo_valor



# print(mapValues(76, 100))