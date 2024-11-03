import pandas as pd
from datetime import datetime, timedelta
import pytz
import random

# Dados dos aviões
dados = {
    'icao24': ['e49408', 'e49405', 'e49443', 'e49446', 'e4811c'],
    'callsign': ['PTGCR', 'GLO2058', 'AZU2733', 'AZU4145', 'PPNNN'],
    'origin_country': ['Brazil'] * 5,
    'on_ground': [True, True, True, True, True],  # Todos os aviões estão no solo inicialmente
    'departure_time': [None] * 5  # Inicialmente sem horário de decolagem
}

# Criar o DataFrame
df_avioes = pd.DataFrame(dados)

# Duração da decolagem em horas
duracao_decolagem = 0.5  # 30 minutos

# Simular decolagem dos aviões
def simular_decolagem(df):
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    for index, row in df.iterrows():
        if row['on_ground']:  # Se o avião está no solo
            df.at[index, 'on_ground'] = False  # O avião decolou
            df.at[index, 'departure_time'] = now  # Atualizar a hora de decolagem

simular_decolagem(df_avioes)

# Exibir o DataFrame após simulação de decolagem
print("DataFrame após simulação de decolagem:")
print(df_avioes[['callsign', 'departure_time', 'on_ground']])

# Exibir horários de decolagem formatados
print("\nHorários de decolagem dos aviões:")
for _, row in df_avioes.iterrows():
    if not row['on_ground']:
        print(f"Voo {row['callsign']} decolou às {row['departure_time'].strftime('%H:%M')}.")
    else:
        print(f"Voo {row['callsign']} está aguardando para decolar.")
