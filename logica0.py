import pandas as pd

# Função para calcular o INSS com base no salário
def calcular_inss(salario):
    if salario <= 1212.00:
        return salario * 0.075
    elif salario <= 2427.35:
        return salario * 0.09
    elif salario <= 3641.03:
        return salario * 0.12
    elif salario <= 7087.22:
        return salario * 0.14
    else:
        return 7087.22 * 0.14  # Teto máximo do INSS para salários superiores a R$ 7.087,22

# Função para calcular o FGTS
def calcular_fgts(salario):
    return salario * 0.08

# Criando um DataFrame com os salários dos funcionários
dados = {
    'Funcionario': ['Alice', 'Bruno', 'Carlos', 'Diana', 'Eduardo'],
    'Salario': [1500.00, 3000.00, 4500.00, 8000.00, 1200.00]
}

df = pd.DataFrame(dados)

# Aplicando as funções para calcular o INSS e o FGTS
df['INSS'] = df['Salario'].apply(calcular_inss)
df['FGTS'] = df['Salario'].apply(calcular_fgts)

print(df)
