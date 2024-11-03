import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import matplotlib.pyplot as plt

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

# Gráfico de Salário Médio por Departamento
plt.figure(figsize=(10, 6))
salario_medio_por_departamento.plot(kind='bar', color='skyblue')
plt.title('Salário Médio por Departamento')
plt.xlabel('Departamento')
plt.ylabel('Salário Médio')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('salario_medio_por_departamento.png')
plt.close()

# Função para criar tabela no PDF
def criar_tabela_pdf(data, c, x, y):
    max_rows_per_page = 25
    rows = [data.columns.tolist()] + data.values.tolist()
    
    for i in range(0, len(rows), max_rows_per_page):
        table = Table(rows[i:i + max_rows_per_page])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        table.wrapOn(c, A4[0], A4[1])
        table.drawOn(c, x, y)
        
        y -= 150  # Ajusta a posição para a próxima tabela
        
        if y < 100:  # Cria uma nova página se necessário
            c.showPage()
            y = 750  # Reseta a posição vertical para o topo da nova página

# Exportar dados e gráfico para PDF
pdf_path = 'analise_funcionarios.pdf'
c = canvas.Canvas(pdf_path, pagesize=A4)

# Título do PDF
c.setFont("Helvetica-Bold", 16)
c.drawString(200, 800, "Análise de Funcionários")

# Dados Brutos
c.setFont("Helvetica", 12)
c.drawString(50, 770, "Dados Brutos dos Funcionários:")
criar_tabela_pdf(df, c, 50, 700)

# Salário Médio por Departamento
c.drawString(50, 500, "Salário Médio por Departamento:")
dados_salario_medio = salario_medio_por_departamento.reset_index()
criar_tabela_pdf(dados_salario_medio, c, 50, 450)

# Inserir o gráfico no PDF
c.drawImage('salario_medio_por_departamento.png', 50, 100, width=500, height=250)

# Salvar o PDF
c.save()

print(f"Análise exportada para {pdf_path}")
