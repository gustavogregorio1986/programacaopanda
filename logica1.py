import pandas as pd

# Carregar dados do arquivo (exemplo CSV)
df = pd.read_csv('funcionarios.csv')

# Limpeza de dados
df.dropna(subset=['Salario', 'Departamento'], inplace=True)
df['Nome'] = df['Nome'].str.strip()

# Cálculo de INSS e criação de coluna derivada
def calcular_inss(salario):
    if salario <= 1212:
        return salario * 0.075
    elif salario <= 2427.35:
        return salario * 0.09
    elif salario <= 3641.03:
        return salario * 0.12
    else:
        return salario * 0.14

df['INSS'] = df['Salario'].apply(calcular_inss)

# Agrupamento por departamento e cálculo de salário médio
salario_medio_por_departamento = df.groupby('Departamento')['Salario'].mean()

# Exportar para Excel com múltiplas abas
with pd.ExcelWriter('analise_funcionarios.xlsx') as writer:
    df.to_excel(writer, sheet_name='Dados Brutos', index=False)
    salario_medio_por_departamento.to_excel(writer, sheet_name='Salario Medio por Departamento')
