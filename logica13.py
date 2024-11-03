import random
import pandas as pd

# Exemplo de dados do DataFrame
data = {
    'icao24': ['abc123', 'def456', 'ghi789'],
    'callsign': ['AAL123', 'DAL456', 'UAL789'],
    'origin_country': ['Brazil', 'Brazil', 'Brazil'],
    'on_ground': [True, True, True],
}

# Criar o DataFrame
df_voos = pd.DataFrame(data)

# Função para atribuir destinos aleatórios
def assign_destinations(df):
    destinos_possiveis = ['SSA', 'SDU', 'GRU', 'CGH', 'BHZ']
    df['destination'] = [random.choice(destinos_possiveis) for _ in range(len(df))]
    return df

# Usar a função para atribuir destinos simulados
df_voos = assign_destinations(df_voos)

# Exibir o DataFrame atualizado
print(df_voos)

