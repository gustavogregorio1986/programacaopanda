import pandas as pd
from datetime import datetime, timedelta
import pytz
import random

# Dados dos aviões (substitua pelos dados reais ou carregue a partir de um arquivo)
dados = {
    'icao24': ['e49408', 'e49405', 'e49443', 'e49446', 'e4811c', 'e49a87', 'e49a39', 'e49a47', 'e4a0a4', 'e4a090'],
    'callsign': ['PTGCR', 'GLO2058', 'AZU2733', 'AZU4145', 'PPNNN', 'AZU2885', 'PSSFG', 'PTB2281', 'N', 'PSSNG'],
    'origin_country': ['Brazil'] * 10,
    'last_position': [1.730663e+09] * 10,  # Exemplo de dados
    'geo_altitude': [9395.46, 11955.78, 1645.92, 1005.84, 1219.20, 152.40, 8404.86, 3581.40, 1104.90, 944.88],
    'on_ground': [True, True, False, False, True, True, False, False, True, False]
}

# Criar o DataFrame
df_avioes = pd.DataFrame(dados)

# Duração dos voos em horas (exemplo)
duracao_voos = {
    'GRU': 1.5,  # 1 hora e 30 minutos
    'BHZ': 2.0,  # 2 horas
    'SDU': 1.0,  # 1 hora
    'CGH': 1.2   # 1 hora e 12 minutos
}

# Atribuir destinos aleatórios para os aviões
def assign_random_destinations(df):
    destinos_possiveis = list(duracao_voos.keys())
    df['destination'] = [random.choice(destinos_possiveis) for _ in range(len(df))]
    return df

df_avioes = assign_random_destinations(df_avioes)

# Calcular a hora de chegada prevista
def calcular_chegada(row):
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    if row['on_ground']:
        return None  # Se o avião estiver no solo, não está a caminho
    else:
        return now + timedelta(hours=duracao_voos[row['destination']])  # Adicionar a duração do voo

# Adicionando uma coluna para a hora de chegada prevista
df_avioes['arrival_time'] = df_avioes.apply(calcular_chegada, axis=1)

# Simular pouso imediato dos aviões
def simular_pouso_imediato(df):
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    for index, row in df.iterrows():
        if not row['on_ground']:
            df.at[index, 'on_ground'] = True  # O avião pousou
            df.at[index, 'arrival_time'] = now  # Atualizar a hora de chegada para o horário atual

simular_pouso_imediato(df_avioes)

# Exibir o DataFrame após simulação de pouso
print(df_avioes[['callsign', 'destination', 'arrival_time', 'on_ground']])

# Exibir as horas de chegada formatadas
print("\nHorários de chegada dos aviões nos seus destinos:")
for _, row in df_avioes.iterrows():
    if row['on_ground']:
        print(f"Voo {row['callsign']} com destino {row['destination']} chegou às {row['arrival_time'].strftime('%H:%M')}.")
    else:
        print(f"Voo {row['callsign']} com destino {row['destination']} está a caminho.")