import pandas as pd
from datetime import datetime, timedelta
import pytz
import random

# Dados dos aviões
dados = {
    'icao24': ['e49408', 'e49405', 'e49443', 'e49446', 'e4811c', 'e49a87', 'e49a39', 'e49a47', 'e4a0a4', 'e4a090'],
    'callsign': ['PTGCR', 'GLO2058', 'AZU2733', 'AZU4145', 'PPNNN', 'AZU2885', 'PSSFG', 'PTB2281', 'N', 'PSSNG'],
    'origin_country': ['Brazil'] * 10,
    'last_position': [1.730663e+09] * 10,
    'geo_altitude': [9395.46, 11955.78, 1645.92, 1005.84, 1219.20, 152.40, 8404.86, 3581.40, 1104.90, 944.88],
    'on_ground': [True, True, False, False, True, True, False, False, True, False]
}

# Criar o DataFrame
df_avioes = pd.DataFrame(dados)

# Verificar os dados iniciais
print("Dados iniciais dos aviões:")
print(df_avioes)

# Duração dos voos em horas
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

# Verificar destinos atribuídos
print("Destinos atribuídos:")
print(df_avioes[['callsign', 'destination']])

# Calcular a hora de chegada prevista
def calcular_chegada(row):
    try:
        now = datetime.now(pytz.timezone('America/Sao_Paulo'))
        if row['on_ground']:
            return None  # Se o avião estiver no solo, não está a caminho
        else:
            return now + timedelta(hours=duracao_voos[row['destination']])  # Adicionar a duração do voo
    except Exception as e:
        print(f"Erro ao calcular chegada: {e}")
        return None

# Adicionando uma coluna para a hora de chegada prevista
df_avioes['arrival_time'] = df_avioes.apply(calcular_chegada, axis=1)

# Verificar aviões "perdidos" (ainda em voo)
df_avioes['status'] = df_avioes['on_ground'].apply(lambda x: 'pousado' if x else 'em voo')

# Verificar o DataFrame após simulação de pouso
print("DataFrame após verificação de status:")
print(df_avioes[['callsign', 'destination', 'arrival_time', 'on_ground', 'status']])

# Exibir as horas de chegada formatadas e status dos aviões
print("\nStatus dos aviões nos seus destinos:")
for _, row in df_avioes.iterrows():
    if row['on_ground']:
        if row['arrival_time'] is not None:  # Verifica se arrival_time não é None
            try:
                formatted_time = row['arrival_time'].strftime('%H:%M')
                print(f"Voo {row['callsign']} com destino {row['destination']} chegou às {formatted_time} (pousado).")
            except Exception as e:
                print(f"Erro ao formatar horário de chegada: {e}")
        else:
            print(f"Voo {row['callsign']} com destino {row['destination']} chegou, mas a hora de chegada não está disponível.")
    else:
        print(f"Voo {row['callsign']} com destino {row['destination']} está a caminho (em voo).")
