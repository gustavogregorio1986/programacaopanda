import requests
import pandas as pd

# URL da API que fornece informações sobre balsas
url = 'https://jsonplaceholder.typicode.com/users'  # Altere para a URL real da sua API

# Fazer a requisição à API
try:
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Converter a resposta JSON em um DataFrame
        balsas_data = response.json()
        df = pd.DataFrame(balsas_data)

        # Exibir o número de balsas recebidas
        print(f"Número de balsas recebidas: {len(df)}")

        # Mostrar o DataFrame
        print(df)
        
        # Exibir informações de localização, se disponíveis
        if 'localizacao' in df.columns:
            print("Localizações das balsas em tempo real:")
            print(df[['id', 'localizacao']])  # Exibir apenas colunas relevantes
        else:
            print("A coluna 'localizacao' não está presente no DataFrame.")
    else:
        print(f"Erro ao acessar a API: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
