import pandas as pd

# Suponha que você tenha um arquivo CSV com os dados das balsas
# dados = pd.read_csv('caminho/para/seu/arquivo.csv')

# Exemplo de dados fictícios
dados = {
    'Estado': ['SP', 'RJ', 'BA', 'MG', 'PR'],
    'Numero_de_Balsas': [10, 15, 7, 12, 9]
}

df = pd.DataFrame(dados)

print(df)
