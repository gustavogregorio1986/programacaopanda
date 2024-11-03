import requests
import pandas as pd

# URL da API que fornece informações sobre balsas
url = 'https://jsonplaceholder.typicode.com/users'  # Altere para a URL real da sua API

# Definir a nova rota
nova_rota = "Rota Nova"

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
        
        # Filtrar balsas que estão disponíveis (presumindo que haja uma coluna 'em_rota' e 'disponivel')
        if 'em_rota' in df.columns and 'disponivel' in df.columns:
            balsas_disponiveis = df[(df['em_rota'] == False) & (df['disponivel'] == True)]  # Filtra apenas as balsas disponíveis
            print(f"Número de balsas disponíveis: {len(balsas_disponiveis)}")
            print("Balsas disponíveis:")
            print(balsas_disponiveis[['id', 'name', 'localizacao']])  # Exibir apenas colunas relevantes
            
            # Adicionando informações de origem e destino
            # Supondo que você tenha colunas 'origem' e 'destino' na API
            if 'origem' in df.columns and 'destino' in df.columns:
                # Atualizar a coluna de rota das balsas disponíveis
                df.loc[balsas_disponiveis.index, 'rota'] = nova_rota
                print(f"\nBalsas agora alocadas na {nova_rota}:")
                
                # Exibir de onde para onde as balsas estão indo
                balsas_disponiveis['destino'] = "Novo Destino"  # Substitua por um valor real ou lógica para determinar o destino
                print(balsas_disponiveis[['id', 'name', 'localizacao', 'rota', 'origem', 'destino']])  # Mostrar as balsas com origem e destino
            else:
                print("As colunas 'origem' ou 'destino' não estão presentes no DataFrame.")
        else:
            print("As colunas 'em_rota' ou 'disponivel' não estão presentes no DataFrame.")
    else:
        print(f"Erro ao acessar a API: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
