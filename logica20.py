import http.client
import pandas as pd
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
    
    # Converter os dados em um DataFrame
    df_voos = pd.DataFrame(dados_voos['states'])
    
    # Ajustar as colunas
    if len(df_voos.columns) == 17:
        df_voos.columns = ['icao24', 'callsign', 'origin_country', 'last_position', 'last_contact',
                           'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity', 
                           'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 
                           'squawk', 'spi', 'position_source']
    else:
        print(f"Erro: Número inesperado de colunas ({len(df_voos.columns)}).")
    
    # Filtrar aviões que estão sobre o Brasil
    df_voos_brasil = df_voos[df_voos['origin_country'] == 'Brazil']
    
    # Exibir o DataFrame dos aviões no Brasil
    print("Dados dos aviões no Brasil:")
    print(df_voos_brasil)
else:
    error_message = response.read().decode()
    print(f"Erro ao acessar a API: {response.status}, Mensagem: {error_message}")
