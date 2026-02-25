# 📊 Projeto Telecom X: Análise de Evasão de Clientes (Churn)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-orange?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen?style=for-the-badge)

Este projeto foca na redução do Churn da **Telecom X**. Unimos uma limpeza técnica rigorosa (ETL) com uma análise de negócios profunda para identificar por que perdemos 26,6% da base e como reverter esse cenário.

---

## 📋 Contexto e Objetivo
A Telecom X enfrenta um desafio de retenção. O custo de adquirir um novo cliente é muito superior ao de manter um atual. 
**Objetivo:** Identificar o "Vale da Morte" (período de maior evasão) e os principais "vilões" (fatores de risco) para sugerir ações preventivas.

---

## ⚙️ Processo de ETL e Engenharia de Dados
A confiabilidade dos insights veio do tratamento rigoroso:

1. **Extração**: Dados brutos via API JSON.
2. **Limpeza**: Tratamento de strings vazias em `Valor_Total` e conversão para `float`.
3. **Tradução**: Dataset 100% mapeado para Português.
4. **Engenharia**: Criação da métrica $Custo\_Diário$:
   $$Custo\_Diário = \frac{Valor\_Mensal}{30}$$
5. **Vetorização**: Conversão binária (0 e 1) em colunas estratégicas para cálculos de correlação.

---

## 📈 Insights de Negócio (EDA)

### 1. Panorama Geral (O Tamanho do Problema)
Identificamos que **26,6%** da base cancelou o serviço (1.869 clientes). 

> **img/grafico_evasao.png**

### 2. O "Vale da Morte" (Churn Precoce)
A análise de permanência revelou um pico alarmante entre o **1º e o 6º mês**. 
* **Insight:** O erro está no início da jornada. O cliente sai antes mesmo de entender o valor do serviço.

### 3. Vilões vs. Heróis da Retenção
* 🚩 **Vilões:** Contratos mensais (sem fidelidade) e pagamento por Cheque Eletrônico.
* 🛡️ **Heróis:** Contratos Bienais e serviços de **Segurança Online**. Clientes com suporte técnico tendem a ser 3x mais leais.

---

## 💡 Recomendações Estratégicas
Com base nos dados, propomos:
1. **Migração Incentivada:** Campanhas para converter planos mensais em anuais/bienais.
2. **Trilha de Sucesso (Onboarding):** Pós-venda preventivo nos meses 2 e 4.
3. **Incentivo ao Débito Automático:** Redução do churn por "esquecimento de fatura" ou atrito manual.
4. **Auditoria de Fibra Ótica:** Investigar instabilidades técnicas onde o churn é maior.

---

## 📁 Estrutura do Repositório
- 📓 `TelecomX_Analise.py`: Script completo com as análises e códigos Matplotlib.
- 📄 `Relatorio_Churn_TelecomX.pdf`: Relatório executivo finalizado para apresentação.
- 💾 `TelecomX_Data.json`: Fonte de dados.

---

## 👤 Autor
**Seu Nome** [LinkedIn](SEU_LINK_AQUI) | [Seu Email]
