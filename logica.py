import pandas as pd

# Criando um DataFrame com uma coluna de números
dados = {
    'Numero': [5, 10, 15, 20, 25]
}

df = pd.DataFrame(dados)

# Calculando o antecessor e o sucessor
df['Antecessor'] = df['Numero'] - 1
df['Sucessor'] = df['Numero'] + 1

print(df)
