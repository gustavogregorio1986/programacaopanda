import http.client
import pandas as pd
import matplotlib.pyplot as plt
import json
import base64

# Configurações iniciais
username = 'gugagregorio'  # Substitua pelo seu nome de usuário
password = 'Avioesaero'  # Substitua pela sua senha

# Criar conexão com a OpenSky Network
conn = http.client.HTTPSConnection("opensky-network.org")

# Definir o cabeçalho de autenticação
auth = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth}',
    'User-Agent': 'Mozilla/5.0'
}

# Fazer a requisição à API
conn.request("GET", "/api/states/all", headers=headers)

# Obter a resposta
response = conn.getresponse()

# Verificar se a requisição foi bem-sucedida
if response.status == 200:
    dados_voos = json.loads(response.read().decode())

    # Imprimir os dados para verificar a estrutura
    print("Dados retornados da API:")
    print(json.dumps(dados_voos, indent=4))  # Formato legível

    # Criar DataFrame
    # Verifique o número de colunas em 'states'
    states = dados_voos['states']
    print(f"Número de colunas em 'states': {len(states[0]) if states else 0}")  # Mostra quantas colunas existem

    # Se você sabe que existem 17 colunas, atualize aqui:
    df_voos = pd.DataFrame(states, columns=[
        'icao24', 'callsign', 'origin_country', 'longitude', 
        'latitude', 'baro_altitude', 'on_ground', 'velocity', 
        'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 
        'squawk', 'spi', 'position_source', 'timestamp', 'other_data'
    ])
    
    # Filtrar aviões que não estão no solo
    df_voos = df_voos[df_voos['on_ground'] == False]

    # Exibir o DataFrame
    print("Dados dos aviões em tráfego:")
    print(df_voos)

    # Criar um gráfico
    plt.figure(figsize=(12, 6))
    plt.scatter(df_voos['longitude'], df_voos['latitude'], s=df_voos['baro_altitude'] / 10, alpha=0.5, c='blue')
    plt.title('Aviões Trafegando no Céu (não no pátio do aeroporto)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)

    # Adicionar anotações para cada avião
    for i in range(len(df_voos)):
        plt.annotate(f"{df_voos['callsign'].iloc[i]} ({df_voos['origin_country'].iloc[i]})", 
                     (df_voos['longitude'].iloc[i], df_voos['latitude'].iloc[i]), 
                     fontsize=9, ha='right')

    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.show()
else:
    error_message = response.read().decode()
    print(f"Erro ao acessar a API: {response.status}, Mensagem: {error_message}")
