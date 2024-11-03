import requests
import pandas as pd

# URL da API JSONPlaceholder para obter usuários
url = 'https://jsonplaceholder.typicode.com/users'

# Fazer a requisição à API
response = requests.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Converter a resposta JSON em um DataFrame
    usuarios_data = response.json()
    df = pd.DataFrame(usuarios_data)

    # Exibir o número de usuários recebidos
    print(f"Número de usuários recebidos: {len(df)}")

    # Mostrar o DataFrame
    print(df)
else:
    print(f"Erro ao acessar a API: {response.status_code}")
