#%%
# Importando Blibliotecas
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %%
# Importando Dados
url = 'https://raw.githubusercontent.com/alura-cursos/challenge2-data-science/refs/heads/main/TelecomX_Data.json'
dados_brutos = pd.read_json(url)
dados = pd.json_normalize(dados_brutos.to_dict(orient="records"))

# %%
# COMPREENDER AS INFORMAÇÕES
print("Colunas originais:", dados.columns.tolist())
print(dados.info())

# %%
# VERIFICAR E CORRIGIR INCONSISTÊNCIAS

#Converter Charges.Total para numérico (espaços vazios viram NaN)
dados["account.Charges.Total"] = pd.to_numeric(dados["account.Charges.Total"], errors="coerce")

# B. Remover linhas com Churn vazio e Charges.Total nulo
dados = dados[dados['Churn'].str.strip() != ''].copy()
dados.dropna(subset=['account.Charges.Total'], inplace=True)

# C. Remover duplicados
dados.drop_duplicates(inplace=True)

#%%
# TRADUZIR COLUNAS E DADOS
traducao_colunas = {
    'id': 'ID_Cliente',
    'Churn': 'Evasao',
    'customer.gender': 'Genero',
    'customer.SeniorCitizen': 'Idoso',
    'customer.Partner': 'Parceiro',
    'customer.Dependents': 'Dependentes',
    'customer.tenure': 'Meses_Contrato_Cliente', # Tenure do cliente
    'phone.PhoneService': 'Servico_Telefone',
    'phone.MultipleLines': 'Multiplas_Linhas',
    'internet.InternetService': 'Servico_Internet',
    'internet.OnlineSecurity': 'Seguranca_Online',
    'internet.OnlineBackup': 'Backup_Online',
    'internet.DeviceProtection': 'Protecao_Dispositivo',
    'internet.TechSupport': 'Suporte_Tecnico',
    'internet.StreamingTV': 'Streaming_TV',
    'internet.StreamingMovies': 'Streaming_Filmes',
    'account.Contract': 'Tipo_Contrato',
    'account.PaperlessBilling': 'Fatura_Digital',
    'account.PaymentMethod': 'Metodo_Pagamento',
    'account.Charges.Monthly': 'Valor_Mensal',
    'account.Charges.Total': 'Valor_Total',
    'account.tenure': 'Meses_Permanencia'
}
dados.rename(columns=traducao_colunas, inplace=True)

# Tradução dos conteúdos das células
mapa_valores = {
    'Yes': 'Sim',
    'No': 'Nao',
    'Month-to-month': 'Mensal',
    'One year': 'Anual',
    'Two year': 'Bienal',
    'Fiber optic': 'Fibra otica',
    'Electronic check': 'Cheque eletronico',
    'Mailed check': 'Cheque correio',
    'Bank transfer (automatic)': 'Transferencia bancaria',
    'Credit card (automatic)': 'Cartao de credito',
    'Female': 'Feminino',
    'Male': 'Masculino'
}
dados.replace(mapa_valores, inplace=True)



# %%
# APLICAÇÃO DO BINÁRIO SELETIVO
# O código abaixo verifica cada coluna: se houver APENAS "Sim" e "Nao", converte.
for col in dados.columns:
    # Pegamos os valores únicos ignorando nulos
    valores_unicos = set(dados[col].dropna().unique())
    
    # Verifica se o conjunto de valores é exatamente {'Sim', 'Nao'} ou subconjunto
    if valores_unicos.issubset({'Sim', 'Nao'}) and len(valores_unicos) > 0:
        print(f"Convertendo coluna binária: {col}")
        dados[col] = dados[col].map({'Sim': 1, 'Nao': 0})

# %%
# CRIAR COLUNA DE CONTAS DIÁRIAS
dados['Custo_Diario'] = (dados['Valor_Mensal'] / 30).round(2)

#%%
dados.describe().T


#%%
# GRÁFICO DE PIZZA
# Preparando os dados
fatias = dados['Evasao'].value_counts()
labels = ['Ficaram (Base Ativa)', 'Saíram (Evasão)']
cores = ['#2ecc71', '#e74c3c'] # Verde e Vermelho

# Criando a figura
plt.figure(figsize=(8, 8))

# Criando o gráfico de pizza (com um furo no meio para virar Donut)
plt.pie(fatias, 
        labels=labels, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=cores, 
        pctdistance=0.85, 
        explode=(0, 0.1), # Destaca a fatia da Evasão
        shadow=True)

# Desenhando um círculo branco no centro (efeito Donut)
centro_circulo = plt.Circle((0,0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centro_circulo)

# Adicionando um comentário centralizado no furo do gráfico
plt.text(0, 0, f'Total Analisado\n{len(dados)} Clientes', 
         ha='center', va='center', fontsize=12, fontweight='bold')

# Adicionando um comentário explicativo ao lado
plt.annotate(f"Atenção:\n{fatias[1]} clientes já\ncancelaram o serviço!", 
             xy=(0.7, 0.5), xytext=(1.3, -0.8),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=11, fontweight='bold', color='#c0392b')

plt.title('Taxa de Evasão Geral - Telecom X', fontsize=16, pad=20)
plt.tight_layout()
plt.show()



# %%
# ANÁLISE DE CORRELAÇÃO E FATORES DE CANCELAMENTO

# Para correlação, transformamos as colunas categóricas restantes em números (Dummies)
dados_analise = pd.get_dummies(dados, columns=['Tipo_Contrato', 'Metodo_Pagamento', 'Servico_Internet', 'Genero'])

# Calculando a correlação com a Evasão
correlacao_evasao = dados_analise.select_dtypes(include=[np.number]).corr()[['Evasao']].sort_values(by='Evasao', ascending=False)

# Transformando em Porcentagem para o Gráfico
correlacao_percentual = correlacao_evasao * 100

# Gerando o Heatmap Percentual
plt.figure(figsize=(10, 12))
annot_labels = correlacao_percentual.map(lambda x: f"{x:.1f}%")

sns.heatmap(
    correlacao_percentual, 
    annot=annot_labels, 
    fmt="", 
    cmap='coolwarm', 
    vmin=-100, vmax=100, center=0
)

plt.title('Influência dos Fatores na Evasão (%)', fontsize=15)
plt.show();

# RESUMO FINAL

print("\n" + "="*30)
print("ETAPA CONCLUÍDA COM SUCESSO")
print("="*30)
print(f"Taxa de Evasão Geral: {round(dados['Evasao'].mean()*100, 2)}%")
print(f"Média de Custo Diário: R$ {dados['Custo_Diario'].mean():.2f}")
print("\nPrincipais Fatores (Top 3 Positivos - Aumentam Churn):")
print(correlacao_percentual.iloc[1:4]) # Exclui a própria Evasão
print("\nPrincipais Fatores (Top 3 Negativos - Retêm Cliente):")
print(correlacao_percentual.tail(3))

# %%
# Gráfico de Barras Empilhadas: O Perfil do Contrato
plt.figure(figsize=(10, 10))
# Criando uma tabela cruzada em porcentagem
ct = pd.crosstab(dados['Tipo_Contrato'], dados['Evasao'], normalize='index') * 100

ax = ct.plot(kind='bar', stacked=True, color=['#2ecc71', '#e74c3c'], figsize=(10,6))

plt.title('Taxa de Evasão por Tipo de Contrato', fontsize=14)
plt.ylabel('Porcentagem (%)')
plt.xlabel('Tipo de Contrato')
plt.legend(title='Evasão', labels=['Não (Ficou)', 'Sim (Saiu)'])
plt.xticks(rotation=0)

# Adicionando rótulos de porcentagem
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    if height > 0:
        ax.annotate(f'{height:.1f}%', (p.get_x() + width/2, p.get_y() + height/2), ha='center', color='black', weight='bold')

plt.show()

# %%
# Histograma de Densidade: (O Tempo)

plt.figure(figsize=(12, 6))
sns.histplot(data=dados, x='Meses_Contrato_Cliente', hue='Evasao', kde=True, element="step", palette=['#2ecc71', '#e74c3c'])

plt.title('Distribuição de Permanência: O Momento da Desistência', fontsize=14)
plt.xlabel('Meses_Permanencia')
plt.ylabel('Quantidade de Clientes')
plt.legend(title='Evasão', labels=['Sim (Saiu)', 'Não (Ficou)'])

plt.show()

#%%
# Ranking de Influência: Vilões vs. O Heróis

# Pegando as correlações e limpando a própria linha da Evasao
ranking = correlacao_percentual.drop('Evasao').sort_values(by='Evasao', ascending=False)

plt.figure(figsize=(10, 8))
cores = ['#e74c3c' if x > 0 else '#3498db' for x in ranking['Evasao']]

sns.barplot(x=ranking['Evasao'], y=ranking.index, palette=cores)

plt.title('Ranking de Impacto na Evasão (%)', fontsize=14)
plt.xlabel('Força da Influência (Positiva = Causa Saída | Negativa = Retém Cliente)')
plt.ylabel('Fatores Analisados')
plt.axvline(0, color='black', linewidth=1) # Linha central

plt.show()

