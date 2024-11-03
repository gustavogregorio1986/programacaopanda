import pandas as pd
from datetime import datetime, timedelta
import pytz

# Dados dos aviões
dados = {
    'icao24': ['abc123', 'def456', 'ghi789'],
    'callsign': ['AAL123', 'DAL456', 'UAL789'],
    'origin_country': ['Brazil', 'Brazil', 'Brazil'],
    'on_ground': [True, True, True],
    'destination': ['GRU', 'BHZ', 'GRU']
}

# Criar o DataFrame
df_avioes = pd.DataFrame(dados)

# Adicionar a coluna de horário real
def get_real_time(destination):
    timezones = {
        'GRU': 'America/Sao_Paulo',
        'BHZ': 'America/Sao_Paulo'
    }
    timezone = pytz.timezone(timezones[destination])
    return datetime.now(timezone).strftime('%H:%M')

df_avioes['time'] = df_avioes['destination'].apply(get_real_time)

# Duração dos voos em horas (exemplo)
duracao_voos = {
    'GRU': 1.5,  # 1 hora e 30 minutos
    'BHZ': 2.0   # 2 horas
}

# Calcular a hora de chegada prevista
def calcular_chegada(row):
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    if row['on_ground']:
        # Se o avião estiver no solo, não está a caminho
        return None
    else:
        # Adicionar a duração do voo à hora atual
        return now + timedelta(hours=duracao_voos[row['destination']])

# Adicionando uma coluna para a hora de chegada prevista
df_avioes['arrival_time'] = df_avioes.apply(lambda row: calcular_chegada(row) if not row['on_ground'] else None, axis=1)

# Exibir o DataFrame
print(df_avioes)

# Filtrar os aviões que estão chegando no seu destino
# Para este exemplo, consideramos que aviões em solo não estão "chegando"
chegando = df_avioes[df_avioes['arrival_time'].notnull()]

print("\nAviões que estão chegando no seu destino:")
print(chegando)