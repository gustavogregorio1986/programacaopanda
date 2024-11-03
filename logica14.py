import pandas as pd
from datetime import datetime
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

# Exibir o DataFrame
print(df_avioes)
