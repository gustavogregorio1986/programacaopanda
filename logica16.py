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

# Filtrar os aviões que estão a caminho (não estão no solo)
df_voos_a_caminho = df_avioes[~df_avioes['on_ground']]

# Agrupar por destino e listar os aviões
if not df_voos_a_caminho.empty:
    agrupados = df_voos_a_caminho.groupby('destination').agg({
        'icao24': lambda x: list(x),  # Lista de icao24
        'callsign': lambda x: list(x),  # Lista de callsign
        'arrival_time': 'first'  # Hora de chegada (pode ser a mesma para todos no grupo)
    }).reset_index()
    
    print("\nAviões que estão chegando nos seus destinos agrupados:")
    print(agrupados)
else:
    print("\nNão há aviões a caminho.")
