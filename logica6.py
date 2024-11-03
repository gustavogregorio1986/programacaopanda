import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurações iniciais
num_avioes = 10  # Número de aviões
np.random.seed(42)  # Para reprodutibilidade

# Gerar dados fictícios
dados_avioes = {
    'id': range(1, num_avioes + 1),
    'nome': [f'Avião {i}' for i in range(1, num_avioes + 1)],
    'latitude': np.random.uniform(low=-90.0, high=90.0, size=num_avioes),
    'longitude': np.random.uniform(low=-180.0, high=180.0, size=num_avioes),
    'altura': np.random.uniform(low=1000, high=12000, size=num_avioes)  # Altura em pés
}

# Criar DataFrame
df_avioes = pd.DataFrame(dados_avioes)

# Exibir o DataFrame
print("Dados dos aviões:")
print(df_avioes)

# Criar um gráfico
plt.figure(figsize=(12, 6))
plt.scatter(df_avioes['longitude'], df_avioes['latitude'], s=df_avioes['altura'] / 100, alpha=0.5, c='blue')
plt.title('Aviões Trafegando no Céu')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)

# Adicionar anotações para cada avião
for i in range(len(df_avioes)):
    plt.annotate(df_avioes['nome'][i], (df_avioes['longitude'][i], df_avioes['latitude'][i]), fontsize=9, ha='right')

plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.axhline(0, color='black',linewidth=0.5, ls='--')
plt.axvline(0, color='black',linewidth=0.5, ls='--')
plt.show()
