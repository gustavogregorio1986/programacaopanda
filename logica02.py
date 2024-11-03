import pandas as pd
import math

# Função para calcular as raízes de uma equação de segundo grau
def calcular_raizes(a, b, c):
    delta = b**2 - 4*a*c
    if delta < 0:
        return ('Sem raízes reais', 'Sem raízes reais')
    else:
        raiz1 = (-b + math.sqrt(delta)) / (2*a)
        raiz2 = (-b - math.sqrt(delta)) / (2*a)
        return (raiz1, raiz2)

# Criando um DataFrame com os coeficientes das equações
dados = {
    'a': [1, 1, 1],
    'b': [-3, -2, 1],
    'c': [2, 1, -1]
}

df = pd.DataFrame(dados)

# Aplicando a função para calcular as raízes
df['Raizes'] = df.apply(lambda row: calcular_raizes(row['a'], row['b'], row['c']), axis=1)

print(df)
