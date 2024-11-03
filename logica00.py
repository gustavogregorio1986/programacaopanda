import pandas as pd
import math

# Função para calcular as raízes de uma equação de segundo grau
def calcular_raizes(a, b, c):
    delta = b**2 - 4 * a * c
    if delta > 0:
        raiz1 = (-b + math.sqrt(delta)) / (2 * a)
        raiz2 = (-b - math.sqrt(delta)) / (2 * a)
        return raiz1, raiz2
    elif delta == 0:
        raiz = -b / (2 * a)
        return raiz, raiz
    else:
        return 'Sem raízes reais', 'Sem raízes reais'

# Criando um DataFrame com os coeficientes das equações
dados = {
    'a': [1, 1, 1, 1],
    'b': [-3, -2, 1, 4],
    'c': [2, 1, -1, 5]
}

df = pd.DataFrame(dados)

# Aplicando a função para calcular as raízes e armazenando o resultado em colunas
df[['Raiz1', 'Raiz2']] = df.apply(lambda row: pd.Series(calcular_raizes(row['a'], row['b'], row['c'])), axis=1)

print(df)
