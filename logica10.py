import http.client
import pandas as pd
import matplotlib.pyplot as plt
import json
import base64
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

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

    # Verificar a estrutura dos dados
    print("Exemplo de dados recebidos:", dados_voos['states'][0])

    # Converter os dados em um DataFrame
    df_voos = pd.DataFrame(dados_voos['states'])

    # Ajustar as colunas
    expected_columns = 17
    if len(df_voos.columns) == expected_columns:
        df_voos.columns = ['icao24', 'callsign', 'origin_country', 'last_position', 'last_contact',
                           'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity', 
                           'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 
                           'squawk', 'spi', 'position_source']
    else:
        print(f"Erro: Número inesperado de colunas ({len(df_voos.columns)}), esperado: {expected_columns}")

    # Filtrar aviões que estão no solo e cujo país de origem é Brasil
    df_voos_no_solo = df_voos[(df_voos['on_ground'] == True) & (df_voos['origin_country'] == 'Brazil')]

    # Verificar se há aviões no solo
    if not df_voos_no_solo.empty:
        # Inicializar geolocalizador
        geolocator = Nominatim(user_agent="geoapiExercises")

        # Função para obter o nome da cidade a partir das coordenadas
        def get_city(latitude, longitude):
            try:
                location = geolocator.reverse((latitude, longitude), exactly_one=True)
                return location.raw['address'].get('city', 'Unknown City')
            except GeocoderTimedOut:
                time.sleep(1)  # Espera 1 segundo antes de tentar novamente
                return get_city(latitude, longitude)
            except Exception as e:
                print(f"Erro ao obter a cidade: {e}")
                return 'Erro ao obter cidade'

        # Adicionar uma nova coluna para as cidades
        df_voos_no_solo['city'] = df_voos_no_solo.apply(lambda row: get_city(row['latitude'], row['longitude']), axis=1)

        # Exibir as cidades únicas onde há aviões no pátio
        cidades_unicas = df_voos_no_solo['city'].dropna().unique()
        print("Cidades com aviões no pátio no Brasil:")
        for cidade in cidades_unicas:
            print(cidade)

        # Criar um gráfico dos aviões no solo no Brasil
        plt.figure(figsize=(12, 6))
        plt.scatter(df_voos_no_solo['longitude'], df_voos_no_solo['latitude'], 
                    s=df_voos_no_solo['baro_altitude'] / 10, alpha=0.5, c='red')
        plt.title('Aviões no Solo no Brasil (pátio do aeroporto)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True)

        # Adicionar anotações para cada avião
        for i in range(len(df_voos_no_solo)):
            plt.annotate(f"{df_voos_no_solo['callsign'].iloc[i]} ({df_voos_no_solo['origin_country'].iloc[i]})", 
                         (df_voos_no_solo['longitude'].iloc[i], df_voos_no_solo['latitude'].iloc[i]), 
                         fontsize=9, ha='right')

        plt.xlim(-180, 180)
        plt.ylim(-90, 90)
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')
        plt.show()
    else:
        print("Não há aviões no solo no Brasil.")
else:
    error_message = response.read().decode()
    print(f"Erro ao acessar a API: {response.status}, Mensagem: {error_message}")
